# ໂມດູນອັບເດດສຳລັບ TouEXManager

repo ນີ້ເກັບ **ໄຟລ໌ຂໍ້ມູນ (payload)** ຂອງແຕ່ລະໂມດູນ ແລະ `index.json` ທີ່ແອັບ Tou EX2 Manager ອ່ານ.

> ⚠️ repo ນີ້**ບໍ່ມີ** source code ແລະ **ບໍ່ມີ key ລົງນາມ** (`platform.pk8` / `platform.x509.pem`) ເດີ້.

## ເລີ່ມຈາກໃສ (ຄັ້ງທຳອິດ)

ສຳລັບລົດຍັງບໍ່ໄດ້ປົດລັອກ: ຍິງ **bootstrap OTA** 1 ຄັ້ງຈາກ USB ແລ້ວຕົວຊ່ວຍຈະຕິດຕັ້ງ
Tou EX2 Manager ໃຫ້ເອງ — ຫຼັງຈາກນັ້ນບໍ່ຕ້ອງໃຊ້ USB/adb ອີກ.

👉 **ຄູ່ມືການຕິດຕັ້ງ (ລາວ + English): [`ota/INSTALL.md`](ota/INSTALL.md)**

> ⚠️ ແພັກນັ້ນໃຊ້ໄດ້ກັບເວີຊັນ **1111** ເທົ່ານັ້ນ (IHU629G, Flyme Auto E 1.8.0).
> Only for software version 1111 — do not flash it on 1114/1121.

## ໂຄງສ້າງ

```
index.json            ລາຍການໂມດູນ: id, ເວີຊັນ, sha256, ຂະໜາດ, ທີ່ຢູ່ໄຟລ໌
payload/
  TouEXManager.apk             ແອັບຈັດການ (ອັບເດດໂຕເອງ)
  GeelyAutoSettings-lao.apk.001 …  ແອັບຕັ້ງຄ່າລົດພາສາລາວ (ແບ່ງເສດ ເພາະ > 100 MB)
  com.flyme.auto.launcher.apk  launcher ພາສາລາວ
  dashpanel.apk                ແຜ່ນ Dashboard
  locale-overlays.zip          overlay ພາສາລາວທັງໝົດ (ໃນ ZIP ມີ <package>.apk)
  keepalive-overlay.apk        ບໍ່ໃຫ້ລະບົບ kill ເພງ
  connect-overlay.apk          ແຖວ Wi-Fi ໃນການຕັ້ງຄ່າ
```

## ວິທີເຮັດໃຫ້ແອັບເຫັນໂມດູນ (ແອັບໃນລົດ)

ແອັບອ່ານ `index.json` ຈາກ URL ທີ່ຕັ້ງໄວ້ໃນໜ້າ ຈັດການລະບົບລົດ → ຊ່ອງ “index.json URL”.

URL ຕົວຢ່າງ (raw ຂອງ repo ນີ້):

```
https://raw.githubusercontent.com/<owner>/<repo>/main/index.json
```

## ການອັບເດດໃນອະນາຄົດ

1. ຢູ່ຄອມພິວເຕີ: ຮັນ `wifisettings\tools\publish-modules.ps1` (ຈະຄິດ `sha256` + ອັບເວີຊັນ + ຂຽນ `index.json`)
2. ອັບໂຫຼດຂຶ້ນຜ່ານ **GitHub Desktop** (commit + push)
3. ໃນລົດ: ເປີດ TouEXManager → “ກວດຫາອັບເດດ” → ກົດເປີດໂມດູນທີ່ຢາກອັບເດດ

ແອັບຈະດຶງໄຟລ໌, ກວດ `sha256`, ແລ້ວຕິດຕັ້ງໃຫ້ເອງ.
