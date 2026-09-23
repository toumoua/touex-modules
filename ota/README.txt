Tou EX2 Setup - bootstrap OTA for the Geely EX2 head unit (IHU629G)
===================================================================

START HERE: INSTALL.md   (step by step, in Lao and in English)

IMPORTANT: for head unit software version 1111 (Flyme Auto E 1.8.0) only.
           Do NOT flash this on version 1114 or 1121.

Files
-----
INSTALL.md                  installation guide, Lao + English (10987 bytes)
3C6025_SW0E22H0128H111100000_user_995.zip
                            delivery container, named and laid out exactly like
                            the factory file
                            (3C6025_SW0E22H0128H111100000_user_995/OS/update.zip)
                            -> extract this folder to the root of a FAT32 USB
                            stick and flash it from the hidden menu
TouEX2Setup-OTA.zip         byte-identical copy of the same container
TouEX2Setup-update.zip      the signed OTA package itself (for
                            --update_package= or advanced use)

sha256
------
container (both names)      03156b66041f58cc55bed6fd5965df110a4e3e5e0ffe557d545383f858430b7f
TouEX2Setup-update.zip      3925095e09ab5555a9d5b16d9a8486b970e7239a9af2fc12cc7f4856bddae202

Sizes: container 858018 bytes, package 857683 bytes.

What it does (it never erases user data)
---------------------------------------
1. checks ro.product.device == IHU629G and aborts on any other unit
2. mounts /system and /data
3. adds persist.adb.tcp.port=5555 to /data/property/persistent_properties, so
   adb over TCP comes back by itself after a factory reset (same shell command
   as the factory package)
4. installs the small bootstrap app into

       /system/app/TouEX2Setup/TouEX2Setup.apk
       /system/etc/default-permissions/com.touex.setup.xml

   NOT priv-app on purpose: /system/app needs no privileged-permission allowlist,
   so the failure mode of 2026-09-18 (a priv-app base plus a different /data/app
   update of the same package) cannot be reproduced by this package.
   Recovery cannot install APKs (it has no PackageManager), but PackageManager
   picks /system/app up on the next boot, so the app is in the car's app list by
   itself - and it survives a factory reset.
5. finishes with "abort" - the message "Installation aborted" is EXPECTED and
   nothing is wiped.

What the bootstrap app then does
--------------------------------
Tou EX2 Setup is a one-screen helper (Lao/English):

  * connect the car to Wi-Fi (in-app picker, with the system Wi-Fi settings as
    fallback),
  * download Tou EX2 Manager from this repository's index.json, verify its
    sha256 and install it silently,
  * disable itself (no launcher icon, no running process) - a factory reset
    brings it back by itself, so a reset never needs this OTA again.

After that everything is managed from Tou EX2 Manager and updated through
index.json in this repository: no USB stick, no adb, no further OTA.
The helper is write-once and is NOT published as a module - never put a copy of
com.touex.setup in /data/app.

Removing it
-----------
* hide it again     : adb shell pm enable com.touex.setup
* remove the apps   : Vehicle settings -> My car -> restore / factory reset
* delete the files  : needs a removal OTA; /system cannot be written at runtime
                      (dm-verity enforcing, bootloader locked)

Credits
-------
The procedure to open the hidden menu and flash from a USB stick comes from the
community blog Dicas Geely EX2:
  https://geelyex2.blogspot.com/2026/07/desbloqueando-central-do-geely-ex2-com.html
  https://geelyex2.blogspot.com/2026/06/como-acessar-o-menu-oculto-da-central.html

Use at your own risk.  Modifying the head unit may affect the vehicle warranty.