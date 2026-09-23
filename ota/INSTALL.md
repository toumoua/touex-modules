# Tou EX2 Setup — ຄູ່ມືການຕິດຕັ້ງ / Installation Guide

> ⚠️ **ສຳລັບ IHU629G, Flyme Auto E 1.8.0, ເວີຊັນ 1111 ເທົ່ານັ້ນ**
> Only for **software version 1111** (IHU629G). ຢ່າຍິງໃສ່ 1114 / 1121.

| ໄຟລ໌ / File | ໃຊ້ເຮັດຫຍັງ / What it is |
|---|---|
| `3C6025_SW0E22H0128H111100000_user_995.zip` | ອັນທີ່ເອົາໄປ USB (ຕົວດຽວກັນກັບ TouEX2Setup-OTA.zip) — extract ໃສ່ USB root |
| `TouEX2Setup-OTA.zip` | ຄືກັນ, ຊື່ສຳຮອງ / same container, alternative name |
| `TouEX2Setup-update.zip` | ຕົວແພັກຂ້າງໃນ (ສຳລັບຄົນທີ່ຮູ້ຈັກ `--update_package=`) |

---

## 🇱🇦 ພາສາລາວ

### ແພັກນີ້ເຮັດຫຍັງ

ຫຼັງຍິງແພັກນີ້ 1 ຄັ້ງ:

1. **ADB ໄຮ້ສາຍ** (ພອດ 5555) ກັບມາໃຊ້ໄດ້ອີກ ຄືກັບແພັກຂອງ GeeKitBR,
2. ຕິດຕັ້ງແອັບນ້ອຍ **Tou EX2 Setup** ໄວ້ໃນ `/system/app` ⇒ **ຢູ່ລອດ factory reset ແລະ ບໍ່ຫາຍ,
   ບໍ່ຄ້າງ, ບໍ່ຕ້ອງຍິງ OTA ຄືນອີກ.**
3. ຕົວຊ່ວຍນັ້ນຈະດຶງ **Tou EX2 Manager** ຈາກ GitHub ມາຕິດຕັ້ງໃຫ້ (ຕ້ອງມີ Wi‑Fi) ແລ້ວປິດໂຕເອງ.
4. ຫຼັງຈາກນັ້ນ **ບໍ່ຕ້ອງໃຊ້ USB ຫຼື ADB ອີກ** — ທຸກຢ່າງ (ໂມດູນພາສາລາວ, ຈໍນ້ອຍ, dash panel …)
   ຈັດການຈາກແອັບ Tou EX2 Manager ແລະ ອັບເດດຈາກ GitHub.

### ກ່ອນເລີ່ມ — ກວດເວີຊັນລົດ

`ຕັ້ງຄ່າລົດ` → ຕົວເລືອກ**ສຸດທ້າຍ** → `ລົດຂອງຂ້ອຍ` → ເບິ່ງເວີຊັນ.
ຕ້ອງເປັນ **1111** (Flyme Auto E 1.8.0). ຖ້າເປັນ 1114 ຫຼື 1121 **ຢ່າຍິງ** — ແພັກນີ້ບໍ່ຮອງຮັບ.

### ຂັ້ນຕອນ

**1. ກະກຽມ USB**
- Format ເປັນ **FAT32** (≤32 GB ໃຊ້ Windows ໄດ້ເລີຍ).
- Extract ໄຟລ໌ zip ທີ່ດາວໂຫຼດມາ ແລ້ວວາງ **folder** ລົງ USB root ⇒ ໂຄງສ້າງຕ້ອງເປັນ:

```text
USB:\
└─ 3C6025_SW0E22H0128H111100000_user_995\
   └─ OS\
      └─ update.zip      <-- ຢ່າແຕະ, ຢ່າ extract
```

**2. ເປີດລົດໄວ້ກ່ອນ** (ຢ່າປະໃຫ້ຈໍດັບ): ຢຽບເບຣກ → ເຂົ້າ D → ກັບມາ P.

**3. ສຽບ USB** → ຈໍຈະຂຶ້ນຂໍ້ຄວາມວ່າຮັບຮູ້ອຸປະກອນ.

**4. ເຂົ້າເມນູລັບ (hidden menu)**
- ປິດ **Bluetooth** ກ່ອນ (ເພື່ອຕັດໂທລະສັບ),
- ເປີດແອັບ **ໂທລະສັບ (Phone)** ເທິງຈໍລົດ,
- ພິມລະຫັດຕາມສູດ: **`#*` (ເດືອນ + 10) (ວັນ) (ໂມງ 12h)** — ແຕ່ລະອັນ 2 ຕົວເລກ

| ຕົວຢ່າງ | ຄິດໄລ່ | ລະຫັດ |
|---|---|---|
| 30/12/2025, 19:25 | 12+10=22, ວັນ 30, 19h→07 | `#*223007` |
| 23/09/2026, 14:10 | 09+10=19, ວັນ 23, 14h→02 | `#*192302` |

(ອ້າງອີງ: <https://geelyex2.blogspot.com/2026/06/como-acessar-o-menu-oculto-da-central.html>)

**5. ຍິງແພັກ** — ໃນເມນູລັບ ໃຫ້ແຕະໄອຄອນ **ອັບເດດຈາກ USB** (ໄອຄອນທີ່ຖືກໄຮໄລ້ສີຂຽວໃນບົດຄວາມ):
<https://geelyex2.blogspot.com/2026/07/desbloqueando-central-do-geely-ex2-com.html>
- ຈໍຈະກວດແພັກ → reboot ເຂົ້າ recovery → ຕິດຕັ້ງເອງ (ບໍ່ຕ້ອງເຮັດຫຍັງ),
- **ຈົບແລ້ວຈະຂຶ້ນ "Installation aborted"** — ອັນນີ້**ປົກກະຕິ**, ເປັນເຈດຕະນາ (ບໍ່ລຶບຂໍ້ມູນຜູ້ໃຊ້),
- ກົດ**ປຸ່ມຍ້ອນເພງກັບຄືນ (◀◀ ຢູ່ພວງມືຊ້າຍ)** ຄ້າງໄວ້ ຈົນຈໍຣີສະຕາດ.

**6. ຫຼັງ reboot — ໃຊ້ຕົວຊ່ວຍ**
- ເປີດແອັບ **Tou EX2 Setup** (ຢູ່ໃນລາຍການແອັບ; ຖ້າບໍ່ເຫັນ ໃຫ້ປັດລາຍການແອັບທັງໝົດ),
- `1. ເຊື່ອມ Wi-Fi ຂອງລົດ` → ເຊື່ອມກັບ Wi‑Fi ບ້ານ ຫຼື hotspot ມືຖື (ຕ້ອງມີອິນເຕີເນັດ),
- `2. ຕິດຕັ້ງ Tou EX2 Manager` → ດາວໂຫຼດຈາກ GitHub ແລ້ວຕິດຕັ້ງເອງ (≈6 MB),
- ຕົວຊ່ວຍຈະ**ປິດໂຕເອງ** (ໄອຄອນຫາຍ) — ຖ້າຢາກປິດເອງກ່ອນ ໃຫ້ຍົກເລີກ checkbox,
- ເປີດ **Tou EX2 Manager** → ເປີດສະວິດໂມດູນທີ່ຕ້ອງການ (ພາສາລາວ, ຈໍນ້ອຍໄທ, dash panel, Wi‑Fi …).

**7. ຫຼັງ factory reset** — ບໍ່ຕ້ອງເຮັດຫຍັງ: ຕົວຊ່ວຍ ແລະ ADB 5555 ກັບມາເອງ,
ແຕ່ແອັບຕ່າງໆທີ່ຢູ່ `/data` ຈະຫາຍ ⇒ ເປີດຕົວຊ່ວຍຄືນ ແລ້ວກົດຕິດຕັ້ງ Manager ອີກຄັ້ງ.

### ຖອຍກັບ / ລຶບອອກ

| ຕ້ອງການ | ເຮັດແນວໃດ |
|---|---|
| ປິດໄວ້ຊົ່ວຄາວ (ໄອຄອນຫາຍ) | ກົດປຸ່ມ `ປິດຕົວຊ່ວຍ` ໃນແອັບ ຫຼື `adb shell pm enable com.touex.setup` ເປີດຄືນ |
| ລຶບແອັບທັງໝົດ (Apps custom + ADB) | `ຕັ້ງຄ່າລົດ` → `ລົດຂອງຂ້ອຍ` → **Restore / ຣີເຊັດໂຮງງານ** |
| ລຶບຕົວຊ່ວຍອອກຈາກ `/system` ໃຫ້ໝົດ | ຕ້ອງຍິງ OTA "removal" — ລຶບໄຟລ໌ໃນ `/system` ຕອນ runtime ບໍ່ໄດ້ (verity ລັອກຢູ່) |

### ຄຳເຕືອນ

- ໃຊ້ກັບ **1111 ເທົ່ານັ້ນ** — ຍິງໃສ່ເວີຊັນອື່ນອາດເຮັດໃຫ້ຈໍຄ້າງ ຫຼື ເສຍການເຮັດວຽກ.
- ຢ່າຖອດ USB ຫຼື ດັບລົດ ລະຫວ່າງຕິດຕັ້ງ.
- ການແກ້ໄຂລະບົບອາດມີຜົນຕໍ່ການຮັບປະກັນ — ຕັດສິນໃຈດ້ວຍໂຕເອງ.

---

## 🇬🇧 English

### What the package does

Flash it **once** and you get:

1. **ADB over Wi‑Fi** (port 5555) again — same idea as the GeeKitBR patch,
2. a tiny app **Tou EX2 Setup** in `/system/app` that **survives a factory reset** and never
   leaves a stuck/broken app behind — no further OTA flash is ever needed,
3. that helper downloads **Tou EX2 Manager** from GitHub and installs it (Wi‑Fi + internet
   required), then disables itself,
4. from then on everything (Lao language modules, Thai cluster, dash panel, …) is managed in
   **Tou EX2 Manager** and updated from GitHub — no USB, no ADB.

### Before you start — check the version

`Vehicle settings` → **last entry** → `My car` → note the software version.
It must be **1111** (Flyme Auto E 1.8.0). **Do not flash on 1114 or 1121** — not supported.

### Steps

**1. Prepare the USB stick**
- Format as **FAT32** (≤32 GB can be formatted by Windows itself).
- Unzip the downloaded file and copy the **folder** to the USB root:

```text
USB:\
└─ 3C6025_SW0E22H0128H111100000_user_995\
   └─ OS\
      └─ update.zip      <-- do NOT extract this file
```

**2. Keep the car awake**: start it (press the brake), shift to **D**, then back to **P**.

**3. Plug the USB in** — the head unit shows that a device was recognized.

**4. Open the hidden menu**
- Switch **Bluetooth off** (so your phone is disconnected),
- open the **Phone** app on the head unit,
- type **`#*` (month + 10) (day) (hour in 12 h)** — two digits each.

| Example | Calculation | Code |
|---|---|---|
| 30/12/2025, 19:25 | 12+10=22, day 30, 19h→07 | `#*223007` |
| 23/09/2026, 14:10 | 09+10=19, day 23, 14h→02 | `#*192302` |

(Source: <https://geelyex2.blogspot.com/2026/06/como-acessar-o-menu-oculto-da-central.html>)

**5. Flash** — in the hidden menu tap the **USB update** icon (the one highlighted in green in the
original article): <https://geelyex2.blogspot.com/2026/07/desbloqueando-central-do-geely-ex2-com.html>
- the unit verifies the package, reboots into recovery and applies it — nothing to do,
- it ends with **"Installation aborted"**: that is **intentional** and normal, user data is not touched,
- hold the **previous-track button** on the left of the steering wheel until the unit restarts.

**6. After the reboot — use the helper**
- Open **Tou EX2 Setup** (in the app list; if it is not there, swipe/open the full app list),
- `1. Connect the car to Wi-Fi` → your home Wi-Fi or a phone hotspot (**internet is required**),
- `2. Install Tou EX2 Manager` → it downloads from GitHub and installs itself (~6 MB),
- the helper then **disables itself** (icon disappears). Uncheck the auto-disable box if you prefer
  to do it manually.
- Open **Tou EX2 Manager** and switch on the modules you want (Lao UI, Thai cluster, dash panel …).

**7. After a factory reset** — nothing to do: the helper and ADB 5555 come back by themselves.
Apps that live in `/data` are gone, so just open the helper and install the manager again.

### Undo / removal

| Goal | How |
|---|---|
| Hide it temporarily | tap `Disable the helper` in the app, or `adb shell pm enable com.touex.setup` to bring it back |
| Remove everything (apps + unlock) | `Vehicle settings` → `My car` → **Restore / factory reset** |
| Delete the helper from `/system` completely | requires a "removal" OTA — runtime writes to `/system` are blocked (dm-verity + locked bootloader) |

### Warnings

- **Version 1111 only.** Flashing on another version can hang the head unit.
- Never unplug the USB or switch the car off during the installation.
- System modifications may affect your warranty — proceed at your own risk.

---

## 🛠 ບັນຫາທີ່ອາດພົບ / Troubleshooting

| ອາການ (Lao) | Symptom (EN) | ວິທີແກ້ / Fix |
|---|---|---|
| `E:Error in /update/update.zip (Status 6)` ແລະ ບໍ່ມີຂໍ້ຄວາມອື່ນເລີຍ | Status 6, no other output | **ແພັກເສຍ (script ອ່ານບໍ່ໄດ້) — ບໍ່ມີຫຍັງຖືກແກ້ໃນລົດ.** ດາວໂຫຼດແພັກໃໝ່ ແລ້ວຍິງຄືນ / re-download the package |
| `Status 7` | Status 7 | ເຄື່ອງບໍ່ຕົງ (device check) → ຜູ້ຜະລິດຕ່າງເວີຊັນ / wrong version |
| ຈໍຄ້າງຢູ່ recovery | Stuck in recovery | ກົດປຸ່ມ **◀◀ (ຍ້ອນເພງກັບຄືນ)** ຄ້າງໄວ້ ~20 ວິນາທີ ຈົນຣີສະຕາດ / hold previous-track |
| ຍິງຜ່ານແລ້ວ ແຕ່ບໍ່ເຫັນແອັບ Tou EX2 Setup | Flash OK but no app icon | ປັດເບິ່ງ**ລາຍການແອັບທັງໝົດ** (ບໍ່ແມ່ນໜ້າຫຼັກ) / open the full app list |
| ຕິດຕັ້ງ Manager ບໍ່ໄດ້ | Cannot install the manager | ກວດວ່າເນັດ**ອອກອິນເຕີເນັດ**ໄດ້ (Wi‑Fi ຕິດ ແຕ່ບໍ່ມີເນັດກໍ່ບໍ່ໄດ້) / needs working internet |

✅ **Status 6 ບໍ່ເປັນອັນຕະລາຍ** — edify ອ່ານ script ກ່ອນ ຈຶ່ງ**ບໍ່ມີຄຳສັ່ງໃດໆຖືກແລ່ນ**:
ທັງ `/system` ແລະ `/data` ຍັງເດີມ ແລະ ລົດ ບໍ່ ມີການປ່ຽນແປງ.
A Status 6 means the updater aborted **before** running any command — nothing was written.

