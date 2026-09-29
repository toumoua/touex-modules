# ໂມດູນອັບເດດສຳລັບ Tou EX2 Manager

repo ນີ້ເກັບ **ໄຟລ໌ຂໍ້ມູນ (payload)** ຂອງແຕ່ລະໂມດູນ ແລະ `index.json` ທີ່ແອັບ Tou EX2 Manager ອ່ານ.

> ⚠️ repo ນີ້**ບໍ່ມີ** source code ເດີ້.

## ເລີ່ມຈາກໃສ (ຄັ້ງທຳອິດ)

ສຳລັບລົດຍັງບໍ່ໄດ້ປົດລັອກ: ຍິງ **bootstrap OTA** 1 ຄັ້ງຈາກ USB ແລ້ວຕົວຊ່ວຍຈະຕິດຕັ້ງ
Tou EX2 Manager ໃຫ້ເອງ — ຫຼັງຈາກນັ້ນບໍ່ຕ້ອງໃຊ້ USB/adb ອີກ.

👉 **ຄູ່ມືການຕິດຕັ້ງ (ລາວ + English): [`ota/INSTALL.md`](ota/INSTALL.md)**

> ⚠️ ແພັກນັ້ນໃຊ້ໄດ້ກັບເວີຊັນ **1111** ເທົ່ານັ້ນ (IHU629G, Flyme Auto E 1.8.0).
> Only for software version 1111 — do not flash it on 1114/1121.

## ໂຄງສ້າງ

```
index.json            ລາຍການ module: id, ເວີຊັນ, sha256, ຂະໜາດ, ທີ່ຢູ່ໄຟລ໌
payload/
  TouEX2Manager.apk             ແອັບຈັດການ (ອັບເດດໂຕເອງ)
  GeelyAutoSettings-lao.apk.*   Settings ພາສາລາວ (APK ແບ່ງເປັນສອງສ່ວນ)
  com.flyme.auto.launcher.apk   launcher ທີ່ປັບປ້າຍຊື່ແອັບ
  dashpanel-platform-signed.apk ແຜ່ນ Dashboard
  ConnAdaptor-touex.apk         patch Android Auto ໄຮ້ສາຍ
  TDashCam-platform.apk         ແອັບກ້ອງບັນທຶກພາບລົດ
  locale-overlays.zip           overlay ພາສາລາວຫຼາຍແອັບ (ໃນ ZIP ມີ APK ຍ່ອຍ)
  keepalive-overlay.apk         overlay ກັນແອັບເພງຖືກປິດ
  connect-overlay.apk           overlay ເພີ່ມແຖວ Wi-Fi ໃນ Settings
  cluster-lang.apk              ຕັ້ງພາສາຈໍ cluster ເປັນໄທ
  TouEXFile.apk                 ຕົວຈັດການໄຟລ໌
  energy-chargebar.apk          ເພີ່ມແຖບຈຳກັດ SOC ໃນໜ້າ Energy
  TouexBrowser.apk              ໄອຄອນ browser ສຳລັບໜ້າ launcher
  microG APKs                   ດຶງຈາກ GitHub ຕາມ URL ໃນ index.json
```

## ອະທິບາຍແຕ່ລະ module

TouEXManager ເປັນແອັບຫຼັກ ສຳລັບອ່ານ `index.json`, ດາວໂຫຼດ payload, ກວດ SHA-256 ແລະຈັດການຕິດຕັ້ງ/ປິດ module. ມັນຢູ່ໃນຊ່ອງ `manager` ຂອງ manifest, ບໍ່ແມ່ນລາຍການໃນ `modules`.

### ພາສາລາວ

- **`settings_lao` — ພາສາລາວໃນ Settings ລົດ:** ຕິດຕັ້ງ GeelyAutoSettings ສະບັບທີ່ແພັດແລ້ວເປັນ system-app update ໃນ `/data`; ເພີ່ມພາສາລາວໃນເມນູເລືອກພາສາ (ແທນພາສາຣັດເຊຍໃນ build ທີ່ຮອງຮັບ). APK ໃຫຍ່ກວ່າ 100 MB ຈຶ່ງແບ່ງເປັນສອງສ່ວນເພື່ອດາວໂຫຼດ. ການປິດຈະກັບໄປໃຊ້ແອັບຕົ້ນສະບັບ.
- **`launcher_lao` — ປ້າຍຊື່ແອັບໃນ launcher:** ອັບເດດ launcher ຂອງລົດໃຫ້ສະແດງຊື່ແອັບເປັນພາສາລາວ ແລະຈັດຄຳຍາວເປັນສອງແຖວ. ຕິດເປັນ update ໃນ `/data`; ປິດແລ້ວກັບໄປຫາ launcher ໃນລະບົບ.
- **`locale_overlays` — ຄຳແປລະບົບ:** ດາວໂຫຼດ ZIP ທີ່ລວມ RRO overlays ປະມານ 34 ແອັບລະບົບ ເຊັ່ນ Settings, launcher, HVAC, Energy, Connectivity, Control Center, Media, Gallery, Framework ແລະ SystemUI. Overlay ເພີ່ມ resource `values-lo` ໂດຍບໍ່ແກ້ APK ຕົ້ນສະບັບ; ປິດແລ້ວປິດ overlay ໄດ້. ຕ້ອງຕັ້ງ locale ລະບົບເປັນ `lo` ຈຶ່ງຈະເຫັນຄຳແປ.

### ລະບົບລົດ ແລະການເຊື່ອມຕໍ່

- **`aa_wireless_patch` — Android Auto ໄຮ້ສາຍ:** ອັບເດດ ConnAdaptor ຂອງລົດດ້ວຍ patch ທີ່ແກ້ການເປີດ Wi-Fi hotspot, ການຕອບອະນຸຍາດເຊື່ອມຕໍ່ Android Auto ແລະບັນຫາ RFCOMM ບາງຈຸດ. ມັນປ່ຽນ system app ເປັນ update ໃນ `/data`; ຄວນໃຊ້ກັບ firmware ທີ່ກົງກັບ build ທີ່ທົດສອບເທົ່ານັ້ນ.
- **`wifi_row` — ແຖວ Wi-Fi ໃນ Settings:** ຕິດຕັ້ງ RRO overlay ເພື່ອເພີ່ມທາງເຂົ້າ Wi-Fi ໃນໜ້າການເຊື່ອມຕໍ່ຂອງການຕັ້ງຄ່າລົດ. ບໍ່ໄດ້ແກ້ Settings APK ໂດຍກົງ ແລະປິດ overlay ໄດ້.
- **`keepalive` — ປ້ອງກັນແອັບເພງຖືກປິດ:** ເພີ່ມແອັບເພງທີ່ຮອງຮັບ (ເຊັ່ນ Spotify, YouTube Music, YouTube ແລະ VLC) ເຂົ້າ whitelist ຂອງ launcher ເພື່ອຫຼຸດບັນຫາເພງຢຸດຫຼັງກົດ Home. ເປັນ RRO ຂະໜາດນ້ອຍ, ປິດໄດ້; launcher ຈະ restart ຫຼັງປ່ຽນສະຖານະ.
- **`cluster_lang` — ພາສາໄທໃນຈໍ cluster:** ປ່ຽນພາສາຂອງຈໍມາດວັດຍ່ອຍ (IPK) ເປັນໄທ ໂດຍສົ່ງລະຫັດພາສາໃຫ້ລະບົບລົດ. ບໍ່ປ່ຽນພາສາ UI ຫຼັກຂອງ Android; ປິດ module ແລ້ວຈໍ cluster ກັບເປັນອັງກິດ.
- **`energy_patch` — ຈຳກັດເປີເຊັນການສາກ:** ເພີ່ມແຖບ native ໃນໜ້າ Energy ໃຫ້ເລືອກເປົ້າໝາຍ SOC 50–100% ແລະເຊື່ອມກັບ TouEXManager ເພື່ອຢຸດ/ເລີ່ມການສາກຕາມຄ່າທີ່ຕັ້ງ. ອັບເດດແອັບ Energy ໃນ `/data`; ການປິດຈະກັບໄປຫາສະບັບ stock. ຮອງຮັບ build ຂອງ Energy ທີ່ patch ກຳນົດໄວ້.
- **`dashpanel` — ແຜ່ນ Dashboard:** ສະແດງຄວາມໄວແບບເຂັມ, ເປີເຊັນແບັດ, ໄລຍະທາງ, ແຮງດັນແບັດ 12V ແລະອຸນຫະພູມນອກ ເປັນພາບພື້ນຫຼັງຢູ່ຫຼັງ widget ລະບົບ. ເປີດແລ້ວຕິດຕັ້ງ/ເປີດໃຊ້ແອັບ dashboard; ປິດແລ້ວລ້າງພາບ dashboard ແລະຊ່ອນແຜ່ນລອຍ.

### ແອັບເສີມ

- **`tdashcam` — ກ້ອງບັນທຶກພາບລົດ:** ສະແດງພາບຈາກກ້ອງ EVS/AVM 4 ຕົວ, ບັນທຶກຄລິບຕໍ່ເນື່ອງລົງ USB ຫຼື storage ໃນເຄື່ອງ, ເບິ່ງຄືນ/ລຶບ/ແບ່ງປັນຄລິບ ແລະເລືອກບັນທຶກສຽງໄດ້. ອອກແບບໃຫ້ກັບມາບັນທຶກຫຼັງ restart ຫຼືຖອດ-ສຽບ USB; ຕ້ອງໃຊ້ APK ທີ່ປ່ອຍທາງການແລະກວດ SHA-256 ກ່ອນຕິດຕັ້ງ.
- **`touex_file` — TouEX File:** file manager ສຳລັບຄົ້ນຫາ ແລະຈັດການໄຟລ໌ໃນ USB ແລະ storage ຂອງລົດ. ເປັນ fork ຈາກ Amaze File Manager 3.8.4; ປັບຊື່/ໄອຄອນໃຫ້ເປັນ TouEX ແລະຖອນທາງເຂົ້າ Root ອອກ ເພາະລະບົບລົດບໍ່ອະນຸຍາດໃຫ້ແອັບໃຊ້ `su`.
- **`browser_app` — ໄອຄອນ browser ໃນ launcher:** ຕິດຕັ້ງແອັບ launcher ຂະໜາດນ້ອຍເພື່ອເພີ່ມໄອຄອນບຣາວເຊີໃນໜ້າຫຼັກລົດ; ເມື່ອເປີດຈະເຂົ້າ browser WebView ທີ່ຢູ່ໃນ TouEXManager. ສະວິດນີ້ເພີ່ມ/ຖອນໄອຄອນ launcher, ບໍ່ໄດ້ລຶບ browser ທີ່ເປີດຈາກ manager.
- **`microg_gms` — microG Services (GmsCore):** ບໍລິການ open-source ທີ່ໃຊ້ແທນບາງສ່ວນຂອງ Google Play Services; payload ດຶງຈາກ GitHub ຂອງ microG.
- **`microg_companion` — microG Companion:** ສ່ວນປະກອບຄູ່ກັບ GmsCore ສຳລັບແອັບ/ບໍລິການທີ່ຄາດຫວັງ package ຂອງ Play Store. ໃຊ້ຄູ່ກັບ GmsCore ຕາມຄວາມຕ້ອງການ.
- **`microg_morphe` — microG RE:** build microG RE ຈາກ Morphe, ມີ package `app.revanced.android.gms`; ອອກແບບໃຫ້ client ທີ່ patch ຂອງ Morphe/Revanced ໃຊ້ສຳລັບລົງຊື່. ROM ລົດບໍ່ມີ signature spoofing, ດັ່ງນັ້ນບໍ່ຄວນຄາດຫວັງວ່າແອັບ Google ທົ່ວໄປທຸກອັນຈະໃຊ້ microG ໄດ້.

> **ຄວາມເຂົ້າກັນໄດ້:** ໂມດູນເຫຼົ່ານີ້ທົດສອບຫຼັກໆເທິງ Geely IHU629G, Android 9 / Flyme Auto E. ໂມດູນທີ່ແທນ system app (ເຊັ່ນ Settings, launcher, ConnAdaptor ແລະ Energy) ອາດຜູກກັບ version ຂອງ firmware ແລະ app ຕົ້ນສະບັບ; ກວດວ່າລົດຢູ່ໃນ version ທີ່ຮອງຮັບກ່ອນໃຊ້.

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
