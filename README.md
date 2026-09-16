# TouEX2Esim — ໂມດູນອັບເດດສຳລັບ TouEXManager

repo ນີ້ເກັບ **ໄຟລ໌ຂໍ້ມູນ (payload)** ຂອງແຕ່ລະໂມດູນ ແລະ `index.json` ທີ່ແອັບ TouEXManager ອ່ານ.

> ⚠️ repo ນີ້**ບໍ່ມີ** source code ແລະ **ບໍ່ມີ key ລົງນາມ** (`platform.pk8` / `platform.x509.pem`) ເດີ້.

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
