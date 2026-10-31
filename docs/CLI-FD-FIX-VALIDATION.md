# Final CLI descriptor fix validation (2026-10-26)

OpenAI Codex was used to make all changes in this follow-up, at sammyz's direction. Earlier work by SavedByLight, TeamWin, AOSP, Qualcomm, and Antigravity is retained and credited in the README and existing platform patches.

## Fix and build

After `twrp unmount /external_sd` and `twrp mount /external_sd`, the exFAT mount completed, but the CLI client and subsequent print clients waited indefinitely for EOF. Inspection showed that exfat-fuse inherited the write handle for `/system/bin/orsout` and the command input handle.

Patch 0005 opens the input with O_CLOEXEC and the output stream with fopen mode "we". This closes those handles on exec, so a filesystem daemon cannot keep the response writer open. Android's pinned Bionic implementation supports this fopen mode. The patch application script includes the new patch. Existing recovery changes were preserved.

- Version: `3.7.1_12-mona-cli-fd-fix`
- Image: `twrp-mona-cli-fd-fix.img`
- Size: 45,465,600 bytes; Android boot header v4, kernel size zero.
- SHA256: `5d9b6900e7098a006e73dc5307b8ac045e1963c3b2e47ea43e775ca4f978260d`
- Build: `lunch twrp_mona-eng; mka -j4 recoveryimage` completed successfully.
- Flashed only `recovery_a`; image bytes verified by readback after USB settled. Active slot remained A.

## Targeted on-device checks: 5 passed, 0 failed

1. Correct recovery version, slot A, Data decrypted, and CE internal storage readable.
2. SD unmount/mount/print cycle 1 returned normally; no ORS input/output handles in exfat-fuse.
3. Same check passed for cycle 2.
4. Same check passed for cycle 3.
5. Recovery-only backup completed after repeated remounts. The full 134,217,728-byte archive matched a live recovery_a read and its TWRP SHA256 digest; its image prefix matched the flashed build. The host copy was verified before the temporary test backup was removed from the SD card.

After another recovery reboot, the version and slot were correct, Data was unlocked, and one additional unmount/mount/print cycle passed. The phone was left in recovery with Data readable and microSD mounted.

## Broader on-device checks: 23 passed, 0 failed

- Recovery identity and boot-control HAL read-only access.
- USB advertises MTP and ADB (configuration check only).
- KeyMint, Gatekeeper, and keystore2 services running.
- Default TWRP logging; custom always-on microSD logger absent.
- Touch input registration, battery sensor, and backlight sensor.
- All six logical EROFS partitions independently mounted read-only and read: system, system_ext, product, vendor, vendor_dlkm, system_dlkm. Temporary mounts were removed afterward.
- Device-encrypted file and credential-encrypted internal-storage reads.
- Temporary write/read/hash checks on DE storage, CE storage, and microSD, followed by scratch-file cleanup.
- Intentional nonexistent mount path returned an expected error and recovery remained responsive.
- Installed recovery readback and image header matched the final artifact.

## Test limits and expected messages

No wipe, format, restore, ROM install, sideload, slot change, or slot-B boot was performed in this validation pass. Earlier documented tests remain historical. Restore functionality, physical touch gestures, end-to-end MTP, USB OTG, fastbootd, and OTA installation are not claimed as tested by this pass. Password-metadata warnings were followed by successful user-0 decryption; USB OTG probes had no attached disk. No private phone logs or backup data are included here.

A first raw capture in the preceding audit had 88 bytes of dd status appended after the partition payload. Separating that status eliminated a false comparison failure; every partition byte matched. Subsequent captures redirect dd status away from image data.
