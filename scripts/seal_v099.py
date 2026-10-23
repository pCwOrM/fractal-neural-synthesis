import os
import shutil
import subprocess
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
vault_name = f"v099_adim3_morpho_onbellek_28ekim_yamasi_sealed_{timestamp}"
vault_dir = os.path.join("/opt/apps/werracle/sealed_vaults", vault_name)

# Previous vault
v098_dir = "/opt/apps/werracle/sealed_vaults/v098_adim1_hasatci_golge_mevboost_rapor_temizligi_sealed_20261023_013311"

print(f"Creating sealed vault: {vault_dir}")
os.makedirs(vault_dir, mode=0o700, exist_ok=True)

# Copy base files from v098
for item in os.listdir(v098_dir):
    if item == "MANIFEST_SHA256.txt":
        continue
    src = os.path.join(v098_dir, item)
    dst = os.path.join(vault_dir, item)
    if os.path.isfile(src):
        shutil.copy2(src, dst)

# Update with freshly patched files
shutil.copy2("/opt/apps/werracle/health/werracle_morpho_golge.py", os.path.join(vault_dir, "werracle_morpho_golge.py"))
shutil.copy2("/opt/apps/werracle/health/werracle_health.py", os.path.join(vault_dir, "werracle_health.py"))
shutil.copy2("/opt/apps/werracle/health/liq_watch.py", os.path.join(vault_dir, "liq_watch.py"))
shutil.copy2("/opt/apps/werracle/reporting/hourly_report_mailer.py", os.path.join(vault_dir, "hourly_report_mailer.py"))
if os.path.exists("/root/measure_svr_margin.py"):
    shutil.copy2("/root/measure_svr_margin.py", os.path.join(vault_dir, "measure_svr_margin.py"))
if os.path.exists("/root/ssh_sertlestirme/svr_margin_measurement_results.json"):
    shutil.copy2("/root/ssh_sertlestirme/svr_margin_measurement_results.json", os.path.join(vault_dir, "svr_margin_measurement_results.json"))

# Generate SHA256 manifest
manifest_path = os.path.join(vault_dir, "MANIFEST_SHA256.txt")
cmd = f"cd {vault_dir} && sha256sum * > MANIFEST_SHA256.txt"
subprocess.run(cmd, shell=True, check=True)

# Set strict permissions 700 / 600
os.chmod(vault_dir, 0o700)
for root, dirs, files in os.walk(vault_dir):
    for f in files:
        os.chmod(os.path.join(root, f), 0o600)

print(f"Sealed vault successfully created and locked (0700/0600): {vault_dir}")

# Verify file count and manifest
manifest_lines = open(manifest_path).readlines()
print(f"Total files verified in manifest: {len(manifest_lines)}")
for line in manifest_lines[:5]:
    print(" ", line.strip())
