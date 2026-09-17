TouEX2Manage OTA package
=======================

Files
-----
TouEX2Manage-OTA.zip        delivery container (same layout as the factory OTA:
                            <name>/OS/update.zip) - copy this one to a USB stick
update.zip                  the signed OTA package itself (for
                            --update_package= or advanced use)

sha256
------
TouEX2Manage-OTA.zip        58d8ac3bb5a81b1d0fd1741c942af6dad1581f08a4634f0c165978209960a77b
update.zip                  28a8dafad161f3e5466f0127fdc50e37f720a3e9e6d1f8b847188d4a37a8e351

What it does (it never erases anything)
---------------------------------------
1. checks ro.product.device == IHU629G
2. mounts /system and /data
3. adds persist.adb.tcp.port=5555 to /data/property/persistent_properties,
   so adb over TCP works again after a factory reset (same shell command as the
   factory package)
4. copies TouEX2Manage.apk to /data/local/tmp/ and to
   /storage/emulated/0/TouEX/ (internal storage)
5. finishes with "abort" - the message "Installation aborted" is EXPECTED and
   nothing was wiped

After the update
----------------
adb connect <unit-ip>:5555
adb shell pm install -r /data/local/tmp/TouEX2Manage.apk

Then open TouEX2Manage and switch on the features you want; every payload is
downloaded from this repository (index.json).

Note
----
The package is signed with the platform key of this head unit (SHA-256
c8a2e9bc...), so the recovery accepts it. Modifying any byte of the zip after
signing invalidates the signature and the update will be rejected.
