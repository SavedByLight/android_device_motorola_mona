from pathlib import Path
import json, re, hashlib
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
errors = []
mods = root / 'recovery/root/lib/modules'
for line in (mods / 'modules.dep').read_text().splitlines():
    if line != line.rstrip():
        errors.append('Trailing whitespace in module dependency list')
    left, right = line.split(':', 1)
    for part in [left, *right.split()]:
        if not (mods / Path(part).name).is_file():
            errors.append('Missing module dependency: ' + part)
for rc in (root / 'recovery/root').glob('*.rc'):
    text = rc.read_text()
    if text.count('${') != len(re.findall(r'\$\{[^}\n]+\}', text)):
        errors.append('Invalid property expansion: ' + rc.name)
lines = [x for x in (root / 'twrp.fstab').read_text().splitlines() if x and not x.startswith('#')]
mounts = set()
for line in lines:
    cols = line.split()
    if len(cols) < 3 or not cols[0].startswith('/'):
        errors.append('Invalid TWRP fstab entry: ' + line)
    if cols[0] in mounts:
        errors.append('Duplicate mount point: ' + cols[0])
    mounts.add(cols[0])
assert (mods / 'goodix_brl_mmi.ko').is_file()
android_lines = [x.split() for x in (root / 'recovery.fstab').read_text().splitlines() if x and not x.startswith('#')]
assert all(len(x) == 5 for x in android_lines)
assert any(x[1:3] == ['/misc', 'emmc'] for x in android_lines)
assert lines[0].startswith('/external_sd ')
assert 'settingsstorage' in lines[0]
assert android_lines[0][1] == '/external_sd'
assert (root / 'recovery/root/system/etc/twrp.fstab').read_bytes() == (root / 'twrp.fstab').read_bytes()
vintf = root / 'recovery/root/vendor/etc/vintf'
assert ET.parse(vintf / 'manifest.xml').getroot().find('sepolicy') is None
boot = ET.parse(vintf / 'manifest/mona-bootctrl.xml').getroot()
assert boot.find('hal/name').text == 'android.hardware.boot'
assert boot.find('hal/transport').text == 'passthrough'
for name in ['android.hardware.boot@1.1.xml', 'android.hardware.boot@1.2.xml']:
    assert ET.parse(vintf / 'manifest' / name).getroot().find('hal') is None
module_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in mods.glob('*.ko')}
report = {'errors':errors,'fstab_entries':len(lines),'module_count':len(module_hashes),
          'module_hashes':module_hashes}
expected = json.loads((root / 'docs/stock-prebuilts.json').read_text())['sha256']
for name, digest in expected.items():
    if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
        errors.append('Stock prebuilt hash mismatch: ' + name)
print(json.dumps({k:v for k,v in report.items() if k!='module_hashes'}, indent=2))
raise SystemExit(bool(errors))
