"""Fine-tune a layer-pruned Lao ASR model, then export it to int8 ONNX.

Pruning xls-r-300m (24 -> N encoder layers) puts the CTC head far out of distribution
(CER ~80%), so the surviving encoder layers + head must be re-adapted on Lao speech.
Works on CPU (slow) and on a GPU (Colab T4: minutes instead of hours).

Data : SiangLao/lao-asr-thesis-dataset   (parquet shards: columns audio{bytes}, text)
Model: SiangLao/xls-r-lao-asr
Out  : model/pruned<N>-ft/            (HF format, reloadable by --from-ckpt)
       model/laoasr-<tag>-int8.onnx   (when --export is given)

Examples
  python finetune-pruned.py --layers 8 --epochs 3 --batch 16 --lr 2e-4 --export p8ft
  python finetune-pruned.py --layers 8 --limit 64 --steps 8 --epochs 1   # smoke test
"""
import argparse
import io
import os
import time

# must be set before torch initialises CUDA: reduces fragmentation on a T4
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

VERSION = "2026-09-26d"
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_ID = "SiangLao/xls-r-lao-asr"
DS = "SiangLao/lao-asr-thesis-dataset"

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import hf_hub_download, list_repo_files
from torch.utils.data import DataLoader, Dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


def shards(split):
    files = [f for f in list_repo_files(DS, repo_type="dataset")
             if f.startswith(f"data/{split}-") and f.endswith(".parquet")]
    return sorted(files)


class Utterances(Dataset):
    """Decodes wav bytes lazily from the (cached) parquet shards."""

    def __init__(self, split, limit=0, max_sec=20.0, min_chars=2):
        import pyarrow.parquet as pq
        self.tables = []
        for name in shards(split):
            path = hf_hub_download(DS, name, repo_type="dataset")
            self.tables.append(pq.read_table(path))
        self.index = []
        for ti, t in enumerate(self.tables):
            for r in range(t.num_rows):
                self.index.append((ti, r))
        self.max_sec = max_sec
        self.min_chars = min_chars
        if limit:
            self.index = self.index[:limit]

    def __len__(self):
        return len(self.index)

    def __getitem__(self, i):
        ti, r = self.index[i]
        row = self.tables[ti].slice(r, 1).to_pylist()[0]
        audio = row["audio"]
        wav, sr = sf.read(io.BytesIO(audio["bytes"]), dtype="float32")
        if wav.ndim > 1:
            wav = wav.mean(axis=1)
        if sr != 16000:
            raise RuntimeError(f"expected 16 kHz, got {sr}")
        wav = wav[: int(self.max_sec * 16000)]
        text = row["text"].strip()
        # wav2vec2 emits one frame per 320 samples: the CTC target must fit inside the audio,
        # otherwise the loss is inf/NaN and one backward pass turns every weight into NaN.
        max_chars = int(len(wav) / 320) - 4
        if max_chars >= 2 and len(text) > max_chars:
            text = text[:max_chars]
        return wav, text


def make_collate(processor):
    """Builds a batch and, crucially, per-sample target lengths.

    Passing one shared (padded) target length tells short utterances that their transcript is
    as long as the longest one in the batch - the CTC loss is then infeasible for them and
    hands back NaN gradients (which destroys the whole model in a single step).
    Samples whose transcript cannot fit into their audio are dropped instead.
    """
    pad_id = processor.tokenizer.pad_token_id

    def collate(batch):
        wavs, texts = [], []
        for w, t in batch:
            t = t.strip()
            if len(t) < 2:
                continue
            ids = processor(text=[t], sampling_rate=16000, return_tensors="pt").input_ids[0]
            frames = len(w) // 320 - 2  # conservative estimate of the encoder output length
            if len(ids) > frames:
                continue
            wavs.append(w)
            texts.append(t)
        if not wavs:
            return None
        feats = processor(wavs, sampling_rate=16000, return_tensors="pt",
                          padding=True, return_attention_mask=False)
        labels = processor(text=texts, sampling_rate=16000,
                           return_tensors="pt", padding=True).input_ids
        lengths = (labels != pad_id).sum(dim=1).clamp(min=1)
        return feats.input_values, labels, lengths

    return collate


def levenshtein(a, b):
    if not a:
        return len(b)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


@torch.no_grad()
def eval_cer(model, processor, ds, device, n=50):
    model.eval()
    err = tot = 0
    for i in range(min(n, len(ds))):
        wav, ref = ds[i]
        x = torch.from_numpy(wav).unsqueeze(0).to(device)
        logits = model(x).logits.float().cpu()
        ids = torch.argmax(logits, dim=-1)[0].tolist()
        pad = processor.tokenizer.pad_token_id
        out, prev = [], None
        for t in ids:
            if t != prev and t != pad:
                out.append(t)
            prev = t
        hyp = processor.tokenizer.decode(out)
        r = "".join(ref.split())
        h = "".join(hyp.split())
        err += levenshtein(r, h)
        tot += max(len(r), 1)
    model.train()
    return 100.0 * err / max(tot, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", type=int, default=8)
    ap.add_argument("--epochs", type=float, default=3)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=1,
                    help="gradient accumulation steps (effective batch = batch * accum)")
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--steps", type=int, default=0, help="cap steps per epoch")
    ap.add_argument("--limit", type=int, default=0, help="cap train rows")
    ap.add_argument("--freeze-fe", type=int, default=1)
    ap.add_argument("--threads", type=int, default=0, help="CPU threads (0 = leave default)")
    ap.add_argument("--eval-n", type=int, default=40, help="rows used for the per-epoch CER")
    ap.add_argument("--max-sec", type=float, default=20.0, help="cap utterance length in seconds")
    ap.add_argument("--out", default="")
    ap.add_argument("--export", default="", help="also export int8 ONNX with this tag")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"finetune-pruned {VERSION} on {device}")
    if device == "cuda":
        print("GPU:", torch.cuda.get_device_name(0))
    elif args.threads:
        torch.set_num_threads(args.threads)

    out = args.out or os.path.join(HERE, "model", f"pruned{args.layers}-ft")
    print(f"loading {MODEL_ID} ...")
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
    model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

    layers = model.wav2vec2.encoder.layers
    if args.layers < len(layers):
        model.wav2vec2.encoder.layers = torch.nn.ModuleList(layers[: args.layers])
        model.config.num_hidden_layers = args.layers
        model.wav2vec2.config.num_hidden_layers = args.layers
    if args.freeze_fe:
        for p in model.wav2vec2.feature_extractor.parameters():
            p.requires_grad = False
        model.wav2vec2.feature_extractor.eval()
        print("feature extractor frozen")

    model.to(device)
    model.train()
    n_train = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"layers={len(model.wav2vec2.encoder.layers)}  trainable={n_train/1e6:.1f}M")

    ds = Utterances("train", limit=args.limit, max_sec=args.max_sec)
    ev = Utterances("test", limit=args.eval_n, max_sec=args.max_sec)
    print(f"train rows: {len(ds)}   eval rows: {len(ev)}")

    dl = DataLoader(ds, batch_size=args.batch, shuffle=True,
                    num_workers=2 if device == "cuda" else 0,
                    pin_memory=(device == "cuda"),
                    collate_fn=make_collate(processor), drop_last=True)

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=0.01)
    steps_per_epoch = args.steps if args.steps else max(1, len(dl))
    accum = max(1, args.accum)
    total = max(1, int(steps_per_epoch * args.epochs))
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=args.lr, total_steps=total,
                                                pct_start=0.15)
    # zero_infinity=False on purpose: with True an infeasible batch reports loss 0 (finite) but
    # hands back NaN gradients, which silently wipes the model.  With False it is Inf and the
    # loop skips that batch.
    ctc = torch.nn.CTCLoss(blank=processor.tokenizer.pad_token_id, zero_infinity=False)
    # The pruned head starts far out of distribution, so the first losses are large and an fp16
    # activation can overflow -> start with a small scale and let the scaler grow it back.
    scaler = torch.amp.GradScaler("cuda", init_scale=512.0, growth_interval=200) if device == "cuda" else None
    use_amp = device == "cuda"

    print(f"plan: {steps_per_epoch} steps/epoch x {args.epochs} epochs = {total} steps")
    print(f"batch={args.batch} accum={accum} (effective {args.batch * accum})  "
          f"max_sec={args.max_sec}", flush=True)
    step, t_start, running, oom = 0, time.time(), 0.0, 0
    for epoch in range(int(np.ceil(args.epochs))):
        for i, batch in enumerate(dl):
            if batch is None:
                continue
            wav, labels, lengths = batch
            wav = wav.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            lengths = lengths.to(device, non_blocking=True)
            try:
                with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=use_amp):
                    logits = model(wav).logits
                log_probs = torch.nn.functional.log_softmax(logits.float(), dim=-1).transpose(0, 1)
                ilen = torch.full((wav.size(0),), log_probs.size(0), dtype=torch.long)
                tlen = lengths
                loss = ctc(log_probs, labels, ilen, tlen)
            except RuntimeError as e:  # CUDA OOM or a shape problem - skip instead of dying
                low = str(e).lower()
                if "out of memory" not in low:
                    raise
                oom += 1
                opt.zero_grad(set_to_none=True)
                if device == "cuda":
                    torch.cuda.empty_cache()
                print(f"  !! CUDA OOM - batch skipped ({oom}) - lower --batch if this repeats",
                      flush=True)
                continue
            if not torch.isfinite(loss):
                print("  !! non-finite loss - batch skipped", flush=True)
                opt.zero_grad(set_to_none=True)
                continue

            if scaler:
                scaler.scale(loss / accum).backward()
            else:
                (loss / accum).backward()
            if (i + 1) % accum != 0:
                continue  # gradient accumulation: step only every accum batches

            if scaler:
                # GradScaler.step() itself skips the update when the gradients hold Inf/NaN and
                # update() then lowers the scale - do NOT skip the step by hand here, that leaves
                # the scaler in an inconsistent state ("unscale_() has already been called").
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scale_before = scaler.get_scale()
                scaler.step(opt)
                scaler.update()
                opt.zero_grad(set_to_none=True)
                if scaler.get_scale() < scale_before:
                    print(f"  !! amp overflow - batch skipped (scale {scale_before:.0f} -> "
                          f"{scaler.get_scale():.0f})", flush=True)
                    continue
            else:
                if not all(p.grad is None or torch.isfinite(p.grad).all()
                           for p in model.parameters()):
                    with torch.no_grad():
                        reps = (labels[:, 1:] == labels[:, :-1]).sum(dim=1)
                        need = (lengths + reps).tolist()
                        bad = sum(1 for p in model.parameters()
                                  if p.grad is not None and not torch.isfinite(p.grad).all())
                    print(f"  !! non-finite gradient - step skipped  loss={loss.item():.4f} "
                          f"ilen={log_probs.size(0)} tlen={tlen.tolist()} min_needed={need} "
                          f"bad_params={bad}", flush=True)
                    opt.zero_grad(set_to_none=True)
                    continue
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                opt.zero_grad(set_to_none=True)

            sched.step()
            running += loss.item()
            step += 1
            if step % 10 == 0:
                el = time.time() - t_start
                mem = f" gpu {torch.cuda.memory_reserved()/1e9:.1f}G" if device == "cuda" else ""
                print(f"  step {step:5d}/{total}  loss {running/10:.3f}  "
                      f"lr {sched.get_last_lr()[0]:.2e}  {el/step:.2f}s/step  "
                      f"eta {(total-step)*el/step/60:.0f} min{mem}", flush=True)
                running = 0.0
            if args.steps and i + 1 >= args.steps:
                break
        if device == "cuda":
            torch.cuda.empty_cache()
        os.makedirs(out, exist_ok=True)
        model.save_pretrained(out)
        processor.save_pretrained(out)
        cer = eval_cer(model, processor, ev, device, n=args.eval_n)
        print(f"epoch {epoch+1}: eval CER {cer:.1f}%  ({(time.time()-t_start)/60:.0f} min) "
              f"saved -> {out}", flush=True)

    if args.export:
        export_onnx(model, processor, args.export, args.layers)
    print("done ->", out)


def export_onnx(model, processor, tag, layers):
    """fp32 ONNX + MatMul/Gemm-only int8 quantization (Conv must stay fp32 for ARM64)."""
    model = model.eval().cpu()

    # 1) non-finite weights break the quantizer ("scale issue"); report and neutralise them
    bad = []
    with torch.no_grad():
        for n, p in model.named_parameters():
            if not torch.isfinite(p).all():
                bad.append(n)
                p.nan_to_num_(nan=0.0, posinf=0.0, neginf=0.0)
    if bad:
        print("WARNING non-finite weights (zeroed):", ", ".join(bad[:8]),
              f"(+{max(0, len(bad)-8)} more)" if len(bad) > 8 else "")

    fp32 = os.path.join(HERE, "model", f"laoasr-{tag}-fp32.onnx")
    int8 = os.path.join(HERE, "model", f"laoasr-{tag}-int8.onnx")
    os.makedirs(os.path.dirname(fp32), exist_ok=True)
    dummy = torch.zeros(1, 16000 * 3)
    print("exporting", fp32)
    torch.onnx.export(model, (dummy,), fp32, input_names=["input_values"],
                      output_names=["logits"],
                      dynamic_axes={"input_values": {0: "batch", 1: "samples"},
                                    "logits": {0: "batch", 1: "frames"}},
                      opset_version=17, do_constant_folding=True, dynamo=False)

    from onnxruntime.quantization import QuantType, quantize_dynamic
    attempts = [
        {"MatMulConstBOnly": True},
        {"MatMulConstBOnly": True, "PerChannel": False},
        {"MatMulConstBOnly": True, "PerChannel": False, "reduce_range": False},
    ]
    last = None
    for i, extra in enumerate(attempts, 1):
        try:
            print(f"quantizing (attempt {i}: {extra})")
            quantize_dynamic(model_input=fp32, model_output=int8,
                             weight_type=QuantType.QInt8,
                             op_types_to_quantize=["MatMul", "Gemm"],
                             extra_options=extra)
            break
        except Exception as e:  # noqa: BLE001 - the quantizer asserts on degenerate weights
            last = e
            print(f"  attempt {i} failed: {type(e).__name__}: {e}")
    else:
        raise RuntimeError(f"quantization failed: {last}")

    for p in (fp32, int8):
        print(f"  {os.path.basename(p)}: {os.path.getsize(p)/1e6:.1f} MB")
    # id <TAB> token, sorted by id - used by the on-device app and by the CER check
    vocab = processor.tokenizer.get_vocab()
    with open(os.path.join(HERE, "model", "vocab.txt"), "w", encoding="utf-8") as f:
        for t, i in sorted(vocab.items(), key=lambda kv: kv[1]):
            f.write(f"{i}\t{t}\n")
    with open(os.path.join(HERE, "model", f"model-info-{tag}.txt"), "w", encoding="utf-8") as f:
        f.write(f"layers={layers}\nfp32={os.path.getsize(fp32)}\nint8={os.path.getsize(int8)}\n")


if __name__ == "__main__":
    main()
