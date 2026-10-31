#!/bin/sh
set -eu
device_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
recovery_dir=${1:-bootable/recovery}
vold_dir=${2:-system/vold}
apply_one() {
    target=$1
    patch=$2
    if git -C "$target" apply --reverse --check "$patch" 2>/dev/null; then
        echo "Already applied: $(basename "$patch")"
    else
        git -C "$target" apply --check "$patch"
        git -C "$target" apply "$patch"
    fi
}
apply_one "$recovery_dir" "$device_dir/patches/0001-settings-storage-and-slot-errors.patch"
apply_one "$recovery_dir" "$device_dir/patches/0002-aidl-gatekeeper-link.patch"
apply_one "$vold_dir" "$device_dir/patches/0003-existing-keys-and-aidl-gatekeeper.patch"
apply_one "$recovery_dir" "$device_dir/patches/0004-super-unmap-all-slots.patch"
apply_one "$recovery_dir" "$device_dir/patches/0005-cli-fifo-close-on-exec.patch"
