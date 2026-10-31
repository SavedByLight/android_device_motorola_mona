#
# Copyright (C) 2025 The Android Open Source Project
# Copyright (C) 2025 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#

# Local mona recovery configuration, based on SavedByLight's android-12.1 tree.
# Hardware layout and modules verified against the connected XT2517-1.
DEVICE_PATH := device/motorola/mona
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_VARIANT := generic
TARGET_CPU_VARIANT_RUNTIME := kryo300
TARGET_NO_BOOTLOADER := true
TARGET_BOARD_PLATFORM := parrot
TARGET_BOOTLOADER_BOARD_NAME := parrot
TARGET_SCREEN_DENSITY := 450

# Stock recovery is a header-v4 ramdisk-only image. Use the installed kernel.
TARGET_NO_KERNEL := true
BOARD_EXCLUDE_KERNEL_FROM_RECOVERY_IMAGE := true
BOARD_BOOTIMG_HEADER_VERSION := 4
BOARD_MKBOOTIMG_ARGS += --header_version 4
BOARD_RECOVERY_MKBOOTIMG_ARGS := --header_version 4
BOARD_RAMDISK_USE_LZ4 := true
BOARD_BOOTIMAGE_PARTITION_SIZE := 100663296
BOARD_RECOVERYIMAGE_PARTITION_SIZE := 134217728
BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 100663296
BOARD_HAS_LARGE_FILESYSTEM := true
BOARD_FLASH_BLOCK_SIZE := 262144
TARGET_COPY_OUT_VENDOR := vendor
BOARD_SUPER_PARTITION_SIZE := 9126805504
BOARD_SUPER_PARTITION_GROUPS := motorola_dynamic_partitions
BOARD_MOTOROLA_DYNAMIC_PARTITIONS_PARTITION_LIST := system system_ext product vendor odm vendor_dlkm
BOARD_MOTOROLA_DYNAMIC_PARTITIONS_SIZE := 9122611200
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/recovery.fstab
TARGET_RECOVERY_DEVICE_DIRS := $(DEVICE_PATH)
TARGET_RECOVERY_PIXEL_FORMAT := RGBX_8888
TARGET_USERIMAGES_USE_EXT4 := true
TARGET_USERIMAGES_USE_F2FS := true
BOARD_HAS_NO_SELECT_BUTTON := true
BOARD_SUPPRESS_SECURE_ERASE := true
RECOVERY_SDCARD_ON_DATA := true
TARGET_RECOVERY_QCOM_RTC_FIX := true

# Android 15 FBEv2 + metadata encryption + hardware-wrapped keys.
TW_INCLUDE_CRYPTO := true
TW_INCLUDE_CRYPTO_FBE := true
TW_INCLUDE_FBE_METADATA_DECRYPT := true
TW_THEME := portrait_hdpi
TW_Y_OFFSET := 100
TW_H_OFFSET := -100
TW_EXTRA_LANGUAGES := true
TW_DEVICE_VERSION := mona-android16-test1
TW_BRIGHTNESS_PATH := /sys/class/backlight/panel0-backlight/brightness
TW_MAX_BRIGHTNESS := 16120
TW_DEFAULT_BRIGHTNESS := 2000
TW_NO_HAPTICS := true
TW_INPUT_BLACKLIST := hbtp_vm
TW_USE_TOOLBOX := true
TW_USE_NEW_MINADBD := true
TW_NO_LEGACY_PROPS := true
TW_EXCLUDE_APEX := true
TW_INCLUDE_REPACKTOOLS := true
TW_INCLUDE_RESETPROP := true
TW_INCLUDE_LIBRESETPROP := true
TW_USE_LEGACY_BATTERY_SERVICES := true
TW_CUSTOM_BATTERY_PATH := /sys/class/power_supply/battery
TW_INCLUDE_LPTOOLS := true
TW_INCLUDE_NTFS_3G := true
TW_INCLUDE_FB2PNG := true
TW_EXCLUDE_DEFAULT_USB_INIT := true
TW_LOAD_VENDOR_BOOT_MODULES := true
TW_LOAD_VENDOR_MODULES := "goodix_brl_mmi.ko adsp_loader_dlkm.ko qti_glink_charger.ko"
TWRP_INCLUDE_LOGCAT := true
TARGET_USES_LOGD := true

# Encrypted data cannot hold settings; keep this path stable during SD probing.
TW_SETTINGS_STORAGE_PATH := /external_sd
