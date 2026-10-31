> **Android 16 compatibility branch:** This branch targets the tested LineageOS
> 23.2 Treble hybrid on mona, using Android 16 System with the stock Motorola
> vendor/kernel. Its build is `3.7.1_12-mona-android16-test1`. The older published
> CLI-fix release below targets stock Android 15 and is not this branch's image.
> See [Android 16 validation](docs/ANDROID16-VALIDATION.md) for the exact checksum,
> passing Data backup and reboot tests, and compatibility limits. Codex was used
> to make these follow-up changes. The exact artifact checksum is recorded in the validation report.

# TWRP device tree for Motorola mona

Moto G Stylus (2025), tested on **XT2517-1** with Android 15
`V2VAS35.29-49-1` and kernel
`6.6.50-android15-8-g0e20c07d648b-ab12946712-4k`.

## Credits and history

This is a fork of [SavedByLight/android_device_motorola_mona](https://github.com/SavedByLight/android_device_motorola_mona),
based on its `android-12.1` commit `6e12663c80cfd49db19dc7882c3d936e5d96b99d`.
SavedByLight's original commits, boot-control/GPT code, initialization work,
and existing file notices are retained. The original generated tree credits
The Android Open Source Project and SebaUbuntu's TWRP device tree generator
(Apache-2.0); Qualcomm/Linux Foundation notices remain in their files.

The [twrpdtgen mona tree](https://github.com/twrpdtgen/android_device_motorola_mona/tree/mona-user-15-V2VAS35V.29-49-ST2.4-6a189-release-keys)
at `0849e7941312418ebb4b8fef5e61c1a3835f16dd` was reviewed for comparison.
It was not the working-tree base and no commits from it were cherry-picked.
Codex was used to make the original fixes and the new integration changes,
at sammyz's direction. The subsequent crypto work also imports the user's
earlier Antigravity QTI service/blob setup; it is credited separately. The
Gatekeeper interface definitions remain AOSP's work, with original notices
and provenance in the platform patch. The resulting recovery was tested on sammyz's phone, with
sammyz confirming touch and clock visibility. TWRP itself is provided by
TeamWin and its contributors.

Stock kernel modules and touch firmware are **prebuilt binaries extracted
from the tested Motorola firmware**, not newly authored driver source.
Their provenance and hashes are in `docs/stock-prebuilts.json`; existing
binary licensing is not replaced by the device-tree source notices.
The old `prebuilt/kernel` and `prebuilt/dtb.img` remain as inherited history
but are not used by this ramdisk-only recovery configuration.

## Build

Use the [minimal TWRP AOSP manifest](https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp)
branch `twrp-12.1`. `docs/platform-manifest.xml` pins the platform revisions
used for the verified build. From a Linux TWRP checkout, place this tree at
`device/motorola/mona`, then run:

```sh
sh device/motorola/mona/tools/apply-recovery-patches.sh
python3 device/motorola/mona/tools/check-tree.py
export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_mona-eng
mka -j4 recoveryimage mona_bootctrl_check
```

Output: `out/target/product/mona/recovery.img`. The stock recovery partition
is 134217728 bytes; header version is 4 and kernel size must be **zero**.
The installed stock kernel must match the bundled modules. This is not a
general compatibility claim for other firmware or model variants.

## Stock Android 15 validation (historical)

See [validation and fix mapping](docs/VALIDATION.md). Touch, microSD,
charging/battery readings, cutout clearance, EROFS mounts, normal Android
reboot, and persistence of recovery were verified on the test device.

**Android 15 Data decryption passed on the tested firmware.** Enter the
existing lock-screen PIN in TWRP: metadata, device-encrypted files and user-0
credential-encrypted internal storage unlocked while System stayed readable.
PIN unlock was repeated after a normal Android boot; the clock was correct.
This is device/firmware-specific, not a general Android 15 support claim. USB initialization parses, but file transfer,
USB OTG, fastbootd, backup/restore and OTA installation have not all received
end-to-end testing. This is an unofficial recovery.

The tested image was installed to recovery_a only, after backing up both
stock recovery slots. Android booted with its original fingerprint and
SELinux Enforcing. A temporary `fastboot boot` attempt entered Android with
the installed normal ramdisk and did not test recovery; validate through
the appropriate recovery partition. Those early stock-firmware checks did not include userdata formatting.
The later Android 16 tests and formatting limitation are documented separately.

## Settings storage and boot-slot follow-up

Recovery preferences are stored on an inserted portable microSD card at
`/external_sd/TWRP/.twrps`, so preferences remain available before PIN unlock. Keep the
card inserted to load/save preferences. The supplied platform patch fixes
an unset settings path and construction of the settings filename in the
pinned TWRP revision. Apply it before building as shown above.

The recovery-only VINTF fragment declares the packaged Qualcomm HIDL boot
control implementation. Previously IBootControl::getService() returned null,
and TWRP misleadingly changed its displayed slot despite failing. The patch
keeps the displayed slot unchanged on HAL errors and shows an explicit slot
error. This is independent of Data decryption.

Codex was used to make all follow-up changes at sammyz's direction.

The recovery-only device manifest also replaces the incompatible stock
Android 15 sepolicy version and the default binder boot HAL fragments.
Only the packaged passthrough implementation is advertised. The Qualcomm
slot enumeration counts boot_a/boot_b exactly, excluding the boot alias.
`mona_bootctrl_check` reports the HAL slot count/current slot without changing
slots; its optional `--set-current` argument reselects the running slot.


## Android 15 decryption and logging

The unlock failure was the older recovery code requesting HIDL Gatekeeper
while the stock phone exposes AIDL. The supplied patches add an opt-in,
verification-only AIDL client and existing-key-only recovery initialization.
They never enroll, reset or replace the lock-screen credential. The PIN must
be entered locally on each recovery boot; it is not stored by these changes.

The patch helper applies the existing recovery patch plus the new recovery
and vold patches, and is safe to run again. Their bases are pinned in
`docs/platform-manifest.xml`: recovery `5c3d206a5eeb3d446bcda8248a405a4b278bab5c`
and vold `a164ba05c5fef288059774a776b2e6e1119957cf`.
Crypto prebuilt provenance/hashes: `docs/stock-crypto-prebuilts.json`.

Logging uses TWRP's default behavior: the active recovery log is
`/tmp/recovery.log`, with the standard TWRP log-saving and manual Copy Log
actions. There is no custom logging daemon, automatic microSD mount loop,
periodic log copying, or forced `/external_sd/twrp_logs` output. A microSD card
is not required for logging. User-requested log export can still target it.

The earlier diagnostic logger was removed because its open logcat file kept
the microSD busy and prevented unmounting, including before SD-card
partitioning/formatting. Existing diagnostic files on a card are not deleted.

System is a read-only EROFS logical partition in Super. The pinned TWRP core
disables individual logical-partition backups and offers raw Super backup;
that is distinct from mount/read access. A Data backup before successful PIN
unlock is incomplete. Full backup/restore and OTA workflows remain untested.
Keep slot A on the tested phone: its existing B Android installation boot-looped.


## Stock Android 15 release (historical)

`3.7.1_12-mona-cli-fd-fix` fixes CLI hangs after mounting the exFAT microSD card by preventing the filesystem daemon from inheriting TWRP command handles. Apply patch 0005 through the patch helper before building. See [the final test report](docs/CLI-FD-FIX-VALIDATION.md) for the image checksum, passing tests, and limits. Codex was used to make all changes in this follow-up. Recovery-only backup passed; restore remains untested.


[Download the final tested recovery image and checksum](https://github.com/sammyz/android_device_motorola_mona/releases/tag/twrp-mona-cli-fd-fix-20261026). The release asset is the exact flashed image, verified by SHA-256 during publication.


## Android 16 compatibility artifact for this branch

Build version: `3.7.1_12-mona-android16-test1` (unofficial prerelease).
Image: `twrp-mona-android16-test1.img`, 45,465,600 bytes.
SHA256: `6d4bdc0a416721f1b5fee763181a3b50c6094f9e09dfda118432c83668b78770`.

This branch targets LineageOS 23.2 System with patch level 2026-10-01 and
stock Motorola Android 15 vendor with patch level 2025-05-01 and the matching
6.6.50 kernel. It is not the full native Android 16 vendor configuration.
Data decryption, a real Data backup, all six logical partition reads, and a
normal Android/recovery reboot cycle passed. Restore is untested. Data backup
excludes internal-storage media. See the [validation and known limitations](docs/ANDROID16-VALIDATION.md),
including the stale userdata mapping issue during Format Data.

Codex was used to make all Android 16 compatibility changes, at the user's
direction. Existing source history, original notices, and prior Antigravity
work are retained and credited above.


Published naming uses `twrp-mona-android16-test1`. The unchanged, previously tested image still reports `3.7.1_12-mona-lineage16-test1` internally; its SHA256 remains unchanged. Source now uses `mona-android16-test1` for subsequent builds. LineageOS references describe the tested ROM, not recovery branding.
