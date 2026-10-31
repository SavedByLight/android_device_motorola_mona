# TWRP for the installed mona LineageOS 23.2 hybrid

OpenAI Codex implemented these changes at the user's direction. Existing
SavedByLight, TeamWin, AOSP, Qualcomm and Antigravity contributions and their
notices are preserved. This is a compatibility variant for the tested current
installation, not a universal claim for all Android 16 ROMs or patch levels.

## Artifact and changes

- Version: `3.7.1_12-mona-android16-test1`.
- Image: `twrp-mona-android16-test1.img`, 45,465,600 bytes.
- SHA256: `6d4bdc0a416721f1b5fee763181a3b50c6094f9e09dfda118432c83668b78770`.
- Installed to recovery_a; active slot A.
- Match running Android release 16 and System patch level 2026-10-01, retain
  the actual stock vendor patch level 2025-05-01, and remove the obsolete boot
  patch alias. The vendor patch in the compiled Lineage Recovery differs from
  the actual installed hybrid's vendor; values were captured from Android.
- Use ext4 read-only/noload for System, System Ext and Product in all three
  fstabs. Preserved vendor partitions continue using EROFS.
- Existing key handling, AIDL Gatekeeper, touch, cutout, default logging and
  CLI close-on-exec fixes remain in place. No credentials were changed.

## Results

The build succeeded. Installed image bytes matched the artifact. The user
confirmed Data is readable, and recovery reports user 0 decrypted.

All 23 non-destructive ADB checks passed: recovery identity, boot-control read
access, advertised USB modes, crypto services, default logging, touch input
registration, battery/backlight sensors, all six logical partition mounts and
reads, DE/CE storage access, temporary write/read/hash checks on DE/CE/microSD,
expected handling of a nonexistent mount, and image/header readback.

A real Data-only backup completed on microSD. All 8 files were copied to F:
and matched fresh source SHA256 hashes. All 3 Data archives matched TWRP's
digests and were fully parsed and their regular-file payloads read without
extracting private contents. Total backup size: 4,046,501,089 bytes; 3,936 tar
entries. Originals remain on microSD. Restore was not performed.

After the backup, LineageOS booted on A with boot_completed=1 and user 0 in
RUNNING_UNLOCKED state. Recovery then booted again, reported user 0 decrypted,
and CE internal storage was accessible. TWRP's normal mount command mounted
System, and its System build-property file was readable alongside Data.

## Limits

Data backup excludes internal-storage media, including photos and Downloads.
This is not a full-device backup, and restore functionality is not claimed as
tested. No wipe, format, metadata erase, credential reset, ROM installation or
slot-B boot was performed during the backup-validation pass above. Future ROM/security-patch changes can require
updating the recovery crypto configuration. Private logs, user backups, raw
metadata and imported agy conversation messages must not be published.

## Local source commits

- `ae3352402cc6b706c13cc5bf244193f82a1348ee`: match the installed crypto values.
- `23b749cb58c7309dc458ca11c32bbac4319df904`: recognize ext4 hybrid partitions.

Publication branch: `mona-android16-recovery`. The commit IDs above identify
local development history, preserved in the source bundle.


## Subsequent clean-install tests and known formatting limitation

Later user-authorized reset and ROM-install experiments are separate from the
successful backup-validation pass above. TWRP Factory Reset completed. Format
Data initially failed because the old `userdata` device-mapper mapping held
the raw block device open. After the filesystem was unmounted and that stale
mapping was removed, Format Data completed successfully. Automatic cleanup of
this case is not fixed by this image. This is a known formatting limitation,
not a claim that all recovery functions have been certified.

The original full unofficial LineageOS ZIP installed through TWRP and was
also sideloaded through matching Lineage Recovery, but bootloops remained.
The separately checked custom hybrid installer booted after a clean format.
These experiments do not isolate the original bootloop's cause, and this
Data-compatibility build does not claim to fix full-ROM or OTA installation.

Only the tested hybrid's user-0 Data access is claimed. Other security-patch
levels, credentials, profiles, firmware variants, and the native full-vendor
Android 16 build require separate validation. Do not infer general Android 16
support from this device-specific configuration.


Published naming uses `twrp-mona-android16-test1`. The unchanged, previously tested image still reports `3.7.1_12-mona-lineage16-test1` internally; its SHA256 remains unchanged. Source now uses `mona-android16-test1` for subsequent builds. LineageOS references describe the tested ROM, not recovery branding.
