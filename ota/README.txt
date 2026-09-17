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
container (both names)      b0f8152fd05d479decdb3d638c8f05c346ce5ed5815ee541ee6bf86808bd2849
update.zip                  d6ff2aba92fe8be1da33b7f47113b5ea821b535476daed9336fcd1a1464bc7b6

Sizes: container 3387078 bytes, update.zip 3386358 bytes.

What it does (it never erases user data)
---------------------------------------
1. checks ro.product.device == IHU629G
2. mounts /system and /data
3. adds persist.adb.tcp.port=5555 to /data/property/persistent_properties,
   so adb over TCP works again after a factory reset (same shell command as the
   factory package)
4. copies TouEX2Manage.apk to /data/local/tmp/ and to
   /storage/emulated/0/TouEX/ (internal storage)
5. installs the app as a system app:
     /system/priv-app/TouEX2Manage/TouEX2Manage.apk
     /system/etc/permissions/privapp_permissions_com.touex.manage.xml
   Recovery cannot install APKs (it has no PackageManager), but PackageManager
   picks /system/priv-app up on the next boot - so after the update the app is
   in the car's app list by itself: no adb, no "pm install", and it survives a
   factory reset.  (The allowlist grants the privileged permissions the app
   asks for; it must list every permission in AndroidManifest.xml or a user
   build can refuse to boot.)
6. finishes with "abort" - the message "Installation aborted" is EXPECTED and
   no user data was touched

To undo step 5 (back to a clean factory state)
---------------------------------------------
adb shell "rm -rf /system/priv-app/TouEX2Manage /system/etc/permissions/privapp_permissions_com.touex.manage.xml"
then reboot, or use the "cleanup" OTA package.

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
