# Hardware validation and fix mapping

Test device: Motorola XT2517-1 (mona), Android 15 V2VAS35.29-49-1.
TWRP: 3.7.1_12-mona-local-verified-layout. These results describe the earlier
hardware-tested build; the publication adds documentation/license comments.

| Symptom | Fix | Verification |
| --- | --- | --- |
| Wrong inherited kernel/layout | Header-v4 ramdisk-only recovery, stock partition sizes | Image header inspection and recovery partition boot |
| Touch unavailable | Matching Goodix module, dependency closure, firmware, modules.dep whitespace, quoted module list | Automatic module loading after reboot; user tested touch |
| Battery incorrectly at 100%, charging unavailable | ADSP/charger modules, modem firmware mount, ADSP start, legacy sysfs battery service | Actual capacity and Charging status; remote processor running |
| EROFS mount permission errors | Explicit read-only mount flags | Runtime mounts passed |
| Reboot returned to recovery | Separate Android v2 recovery.fstab and TWRP v1 twrp.fstab, valid misc entry | BCB command cleared; Android normal boot passed |
| microSD not detected | mmcblk1p1 primary, mmcblk0p1 alternate | FAT32 card mounted at /external_sd, about 29 GB available |
| Center time obscured by camera | 100-pixel theme offset/height correction | User confirmed clock visibility and touch |
| Invalid USB init expansion | Close truncated sys.usb.config property | Init verifier passed |

Source validation: 16 TWRP fstab entries, 268 modules, no missing dependency
files or malformed property expansions. Init scripts passed host_init_verifier.
Packaged module hashes were checked against the captured stock files.

Verified image size: 37965824 bytes; kernel size 0; ramdisk size 37957178.
SHA-256: `1c2f5c6659715b84ab7a5f1474ceb23f67bd14b15f965a84a39c2e0fb7b859fe`.
Installed bytes were read back and matched. Normal Android startup and
recovery persistence passed; Android SELinux was Enforcing.

Encrypted /data remains unsupported. RTC accuracy, USB OTG, backup/restore,
fastbootd, and OTA flashing are not claimed as fully tested.
Private phone logs, serial identifiers, recovery backups and host/VM data
are intentionally excluded from this source contribution.

## Settings and boot-control follow-up

Codex was used to make all follow-up changes at sammyz's direction.
Verified version: `3.7.1_12-mona-settings-slot-fix`.

- Fixed the unset settings-storage variable and malformed filename in the
  pinned TWRP source. An explicit `TW_SETTINGS_STORAGE_PATH` keeps the SD path
  stable when card detection is late after a warm reboot; mount retries are
  bounded. Settings use `/external_sd/TWRP/.twrps`. A saved clock-format
  setting loaded after reflashing, was changed back to its original value,
  then survived another recovery reboot. The card must stay inserted.
- The stock Android 15 vendor manifest contains a sepolicy version that the
  Android 12 recovery libvintf cannot parse. A recovery-only manifest and
  passthrough boot-control declaration replace it, and conflicting default
  binder boot HAL fragments are neutralized. The native diagnostic reports
  `slots=2 current=0` after recovery reboot, with no in-memory manifest edits.
- Qualcomm slot enumeration now excludes the unsuffixed boot alias. The
  current A slot was reselected successfully through the HAL. Failed HAL
  operations now return without changing the displayed slot.
- The user selected B in the GUI; fastboot confirmed B became active. B's
  Android installation boot-looped. Fastboot restored A; normal Android
  startup, original fingerprint and SELinux Enforcing were verified. Slot B
  is not validated as bootable, and its images were not modified. TWRP is
  installed in recovery_a only. Slot selection is not a backup/restore tool.

Final follow-up image: 37974016 bytes, header v4, kernel size zero.
SHA-256: `2be94778a3d4aca2a771b41060934dd9cb52c8d391ec075bb7fe490dfd95f65e`.
Recovery partition readback matched after Android startup. Packaged fstabs,
VINTF declarations, diagnostic and all stock prebuilt hashes were checked.
The recovery build, source checker and git diff --check passed.

This contribution includes the required platform patch under `patches/`;
apply it with `tools/apply-recovery-patches.sh` before building the pinned
TWRP revision. The script supports repeat application without duplicating
changes. Android 15 /data decryption remains unsupported.


## Android 15 crypto follow-up (2026-10-26)

Image: `twrp-mona-aidl-unlock.img`, SHA256
`3225e9aee36b6c27de92a0d748f711f84b806ad1e99b180ccb644d96336db8dc`.
Version `3.7.1_12-mona-aidl-unlock`; recovery A readback matched the image.

- Metadata mapper and existing DE keys loaded during normal recovery startup.
- Stock AIDL Gatekeeper verified the user's PIN and Keystore accepted its token.
- `twrp.user.0.decrypt=1`; internal Android storage directory readable.
- Actual reads from System build.prop and Data packages.xml passed together.
- PIN unlock repeated after normal Android A startup; original fingerprint and
  SELinux Enforcing were verified. User confirmed the clock remained correct.
- The earlier diagnostic build started continuous microSD logs automatically;
  this behavior is superseded by the default-logging follow-up below.
- Source checks retain all 268 module hashes, matching TWRP fstab copies,
  first-position microSD settings storage and boot-HAL manifest checks.

These results supersede earlier notes that Data decryption was unsupported.
They do not validate other firmware, secondary users, OTA, or full restore.
Individual System backup is disabled by upstream Prepare_Super_Volume; raw
Super backup remains the existing option. Do not equate mount success or a
nonzero Data backup size with complete backup/restore validation.

Codex implemented the new recovery integration and logger. The earlier
Antigravity crypto setup is imported with attribution. AOSP Gatekeeper source
and SavedByLight history/notices remain credited to their original authors.


## Default logging follow-up

The custom microSD logger held a logcat output file open, preventing TWRP
from unmounting the card before partitioning/formatting. Remove its init start
action, service definition and shell script, retaining TWRP's own logging.
The active log remains `/tmp/recovery.log`; standard persistence and manual
Copy Log actions remain managed by the unchanged TWRP core.

This change does not alter Data decryption, settings storage or raw Super
backup behavior. FAT32's single-file limit still prevents a single 9.61 GiB
Super image on the tested card. No card formatting is part of validation.

Verified image: `twrp-mona-default-logging.img`, SHA256
`1ce07926684d478a5b9db2c4f23dfed149e3d5e63a5a4aaee8d3a9e94a59fa7a`; version `3.7.1_12-mona-default-logging`.

- Recovery A flash readback matched the image. No other partition was flashed.
- Packaged logger script/init service absent; all 321 prebuilt hashes
  and packaged fstabs matched the source.
- Default `/tmp/recovery.log` existed and grew during recovery operations.
- No custom logger service, script, temporary marker or current-boot microSD
  log directory existed.
- TWRP unmounted the card successfully, it stayed unmounted, then remounted.
- The user confirmed PIN unlock; user-0 internal storage and actual Data/System
  file reads passed together after installing this build.
- No SD formatting, userdata wipe, full backup/restore or OTA test was performed.
Codex was used to make this follow-up at sammyz's direction.


## Dynamic partition unmapping and snapshot merge check follow-up

When checking pending merges or performing a wipe on Virtual A/B devices,
TWRP previously unmapped only active-slot partitions from its mount list,
leaving inactive slot devices (e.g., `system_b` and `-cow` devices) active in
Device Mapper. Subsequent snapshot verification passes failed with EBUSY
("Device or resource busy").

Enumerate all Super metadata partitions across both slots and unmap them
via DeviceMapper before SnapshotManager verifies pending merges. Retain
Android's snapshot manager wipe guard completely intact without bypassing
or deleting OTA metadata records. Statically link `libdm` in recovery.
Add a null file pointer check in `gui.cpp` for `orsout` to prevent FORTIFY
aborts on rapid CLI interactions.

Verified image: `twrp-mona-merge-check-fix.img`, SHA256
`eadb2fdce2066dd781ddd2e318bc6b07dd3c9da3f0fe44525c7c3880230b27b1`; version `3.7.1_12-mona-merge-check-fix`.

- Recovery A flash readback matched the image. No other partition was flashed.
- Unit test suite `test-merge-unmap.py` passed with failure-injection stubs.
- On-device test: "Merge Snapshots" cleanly unmapped `product_a`, `system_a`,
  `system_b`, `system_dlkm_a`, `system_ext_a`, `vendor_a`, and `vendor_dlkm_a`,
  and completed snapshot verification with status 0.
- On-device test: Format Data completed with `make_f2fs -g android` and clean
  checkpoint verification (status 0).
- User PIN unlock, Data decryption (AIDL Gatekeeper), microSD mounts, and RTC
  accuracy remained verified.
Codex and Antigravity (agy) were used to make this follow-up at sammyz's direction.


## Final exFAT CLI mount fix

See [final build and validation results](CLI-FD-FIX-VALIDATION.md): 23 general checks, 5 targeted checks, and a passing post-reboot remount check. Codex was used to make all changes in this follow-up.
