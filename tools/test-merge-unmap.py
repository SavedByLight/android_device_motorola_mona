"""Compile the actual patched cleanup body against failure-injection stubs."""
from pathlib import Path
import subprocess as sp, tempfile, sys
core=Path(sys.argv[1] if len(sys.argv)>1 else 'bootable/recovery')
s=(core/'partitionmanager.cpp').read_text()
start=s.index('bool TWPartitionManager::Unmap_Super_Devices() {')
end=s.index('\n\nbool TWPartitionManager::Check_Pending_Merges()',start)
body=s[start:end]
stub=r'''
#include <cassert>
#include <cstdint>
#include <memory>
#include <set>
#include <string>
#include <vector>
#include <iostream>
#define TW_EXCLUDE_APEX
#define LOGERR(...) do {} while (0)
#define LOGINFO(...) do {} while (0)
static std::set<std::string> maps;
static std::string failure, suffix="_a";
static bool have_metadata=true, mount_busy=false;
static int deleted=0, unmount_calls=0, remove_calls=0;
static uint32_t metadata_slot=99;
static std::vector<std::string> names={"product_a","product_b","system_a","system_b","vendor_a","vendor_b"};
namespace android {
namespace base { std::string GetProperty(const std::string&,const std::string&) { return suffix; } }
namespace fs_mgr {
struct Metadata { std::vector<std::string> partitions=names; };
std::unique_ptr<Metadata> ReadMetadata(const std::string&,uint32_t slot) {
 metadata_slot=slot;
 return have_metadata ? std::make_unique<Metadata>() : nullptr;
}
std::string GetPartitionName(const std::string& n) { return n; }
}
namespace dm {
enum class DmDeviceState { INVALID, ACTIVE };
struct DeviceMapper {
 static DeviceMapper& Instance() { static DeviceMapper d;return d; }
 DmDeviceState GetState(const std::string& n) { return maps.count(n)?DmDeviceState::ACTIVE:DmDeviceState::INVALID; }
};
}}
std::string fs_mgr_get_super_partition_name(uint32_t) { return "super"; }
bool DestroyLogicalPartition(const std::string& n) {
 ++remove_calls;
 if (n==failure) return false;
 return maps.erase(n)==1;
}
struct TWPartition {
 bool Is_Super;
 std::string path;
 bool UnMount(bool) { ++unmount_calls;return !mount_busy; }
 std::string Get_Mount_Point() { return path; }
 ~TWPartition() { ++deleted; }
};
struct TWPartitionManager {
 std::vector<TWPartition*> Partitions;
 bool Unmap_Super_Devices();
 ~TWPartitionManager() { for(auto* p:Partitions)delete p; }
};
static void seed(TWPartitionManager& pm) {
 maps={"product_a","system_a","system_b","vendor_a","vendor_b","system_b-cow","userdata"};
 failure="";suffix="_a";have_metadata=true;mount_busy=false;
 deleted=unmount_calls=remove_calls=0;metadata_slot=99;
 pm.Partitions={new TWPartition{true,"/product"},new TWPartition{true,"/system_root"},
 new TWPartition{true,"/vendor"},new TWPartition{false,"/data"}};
}
'''
tests=r'''
int main() {
 { TWPartitionManager pm;seed(pm);
   assert(pm.Unmap_Super_Devices());
   assert(maps==std::set<std::string>{"userdata"});
   assert(pm.Partitions.size()==1 && !pm.Partitions[0]->Is_Super && deleted==3);
   assert(metadata_slot==0);
 }
 { TWPartitionManager pm;seed(pm);failure="system_b";
   assert(!pm.Unmap_Super_Devices());
   assert(deleted==0 && pm.Partitions.size()==4 && maps.count("system_b"));
   failure="";assert(pm.Unmap_Super_Devices());
   assert(maps==std::set<std::string>{"userdata"});
 }
 { TWPartitionManager pm;seed(pm);have_metadata=false;
   assert(!pm.Unmap_Super_Devices());
   assert(deleted==0 && pm.Partitions.size()==4 && remove_calls==0 && unmount_calls==0);
 }
 { TWPartitionManager pm;seed(pm);mount_busy=true;
   assert(!pm.Unmap_Super_Devices());
   assert(deleted==0 && pm.Partitions.size()==4 && remove_calls==0);
 }
 { TWPartitionManager pm;seed(pm);maps={"userdata"};
   assert(pm.Unmap_Super_Devices());
   assert(remove_calls==0 && maps==std::set<std::string>{"userdata"});
 }
 { TWPartitionManager pm;seed(pm);suffix="_b";
   assert(pm.Unmap_Super_Devices() && metadata_slot==1);
   assert(maps==std::set<std::string>{"userdata"});
 }
 { TWPartitionManager pm;seed(pm);suffix="_invalid";
   assert(!pm.Unmap_Super_Devices());
   assert(deleted==0 && remove_calls==0 && unmount_calls==0);
 }
 std::cout << "PASS: both slots/COW, partial-failure retry, metadata/mount failures, missing maps, B slot, invalid slot\n";
}
'''
with tempfile.TemporaryDirectory(prefix='mona-unmap-test-') as folder:
    root=Path(folder);cpp=root/'test.cpp';exe=root/'test'
    cpp.write_text(stub+'\n'+body+'\n'+tests)
    sp.run(['g++','-std=c++17','-Wall','-Wextra','-Werror',str(cpp),'-o',str(exe)],check=True)
    sp.run([str(exe)],check=True)
