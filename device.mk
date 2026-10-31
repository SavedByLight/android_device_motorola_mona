#
# Copyright (C) 2025 The Android Open Source Project
# Copyright (C) 2025 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#

# Device-specific recovery packages; retain stock dynamic partition support.
LOCAL_PATH := device/motorola/mona
PRODUCT_BUILD_RECOVERY_IMAGE := true
PRODUCT_BUILD_BOOT_IMAGE := false
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota.mk)
PRODUCT_USE_DYNAMIC_PARTITIONS := true
AB_OTA_UPDATER := true
AB_OTA_PARTITIONS := boot init_boot vendor_boot recovery dtbo vbmeta vbmeta_system system system_ext product vendor vendor_dlkm system_dlkm odm
PRODUCT_OTA_ENFORCE_VINTF_KERNEL_REQUIREMENTS := false
PRODUCT_PACKAGES += android.hardware.boot@1.1-impl-qti.recovery bootctrl.parrot.recovery
PRODUCT_PACKAGES += android.hardware.fastboot@1.0-impl-mock fastbootd
PRODUCT_PACKAGES += update_engine_sideload update_verifier
PRODUCT_SHIPPING_API_LEVEL := 30
PRODUCT_TARGET_VNDK_VERSION := 30
PRODUCT_SOONG_NAMESPACES += $(LOCAL_PATH)
