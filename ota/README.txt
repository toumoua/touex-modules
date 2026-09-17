TouEX2Manage OTA package
=======================

Files
-----
3C6025_SW0E22H0128H111100000_user_995.zip
                            delivery container, named and laid out exactly like
                            the factory file (3C6025_SW0E22H0128H111100000_
                            user_995/OS/update.zip) - copy this one to a USB
                            stick
TouEX2Manage-OTA.zip        byte-identical copy of the same container
update.zip                  the signed OTA package itself (for
                            --update_package= or advanced use)

sha256
------
container (both names)      937b4c91987fe2c8ee2470852063d8fd710ab8f33c18e87b97d66a2b0ada766d
update.zip                  11fc8caa2a50af1fdc13759492da0beb5a09b7cf9faf721430fe6addb7441a1e

Sizes: container 3385572 bytes, update.zip 3384852 bytes.

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

META-INF/com/google/android/updater-script MUST use LF line endings only.
The edify lexer understands " ", tab and LF; a CR is an unknown token, so the
script fails to parse and the updater exits with code 6. Recovery then shows
"E:Error in /update/update.zip (Status 6)" and not a single command (not even
ui_print) runs. Status 7 instead is the normal, intentional abort() at the end
of this script.

Recovery exit codes of the update-binary:
  3 = package could not be mapped/opened
  4 = updater-script missing
  5 = updater-script could not be read
  6 = updater-script parse error
  7 = script aborted (abort() called - expected here)

The unit's MTK recovery has a trimmed edify function table: set_perm,
set_perm_recursive, package_extract_dir and delete_recursive are NOT available
(calling one aborts the script with Status 7), so permissions are set with
chmod inside run_program. build-ota.ps1 verifies every function against
update-binary and rejects CR bytes automatically.
