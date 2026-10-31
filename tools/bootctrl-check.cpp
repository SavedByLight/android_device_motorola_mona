// Codex was used to make this diagnostic at sammyz's direction.
#include <android/hardware/boot/1.0/IBootControl.h>
#include <cstdio>
#include <cstring>

int main(int argc, char** argv) {
    using android::hardware::boot::V1_0::IBootControl;
    using android::hardware::boot::V1_0::CommandResult;
    auto hal = IBootControl::getService();
    if (hal == nullptr) {
        std::fprintf(stderr, "Boot control HAL unavailable\n");
        return 1;
    }
    auto current = hal->getCurrentSlot();
    auto count = hal->getNumberSlots();
    if (!current.isOk() || !count.isOk()) return 2;
    unsigned slot = current;
    std::printf("slots=%u current=%u\n", static_cast<unsigned>(count), slot);
    if (argc == 2 && std::strcmp(argv[1], "--set-current") == 0) {
        bool success = false;
        auto result = hal->setActiveBootSlot(slot, [&](const CommandResult& r) {
            success = r.success;
            std::printf("set-current success=%d message=%s\n", r.success, r.errMsg.c_str());
        });
        return result.isOk() && success ? 0 : 3;
    }
    return argc == 1 ? 0 : 4;
}
