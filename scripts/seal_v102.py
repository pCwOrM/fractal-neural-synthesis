import os
import shutil
import subprocess
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
vault_name = f"v102_morpho_hygiene_ve_stable_revert_sealed_{timestamp}"
vault_dir = os.path.join("/opt/apps/werracle/sealed_vaults", vault_name)

# Previous vault
v101_dir = "/opt/apps/werracle/sealed_vaults/v101_dis_denetci_adim1_2_3_dogrulandi_sealed_20261023_023136"

print(f"Creating sealed vault: {vault_dir}")
os.makedirs(vault_dir, mode=0o700, exist_ok=True)

# Copy base files from v101
for item in os.listdir(v101_dir):
    if item == "MANIFEST_SHA256.txt":
        continue
    src = os.path.join(v101_dir, item)
    dst = os.path.join(vault_dir, item)
    if os.path.isfile(src):
        shutil.copy2(src, dst)

# Update with freshly patched files
shutil.copy2("/opt/apps/werracle/health/werracle_morpho_golge.py", os.path.join(vault_dir, "werracle_morpho_golge.py"))
shutil.copy2("/opt/apps/werracle/health/werracle_health.py", os.path.join(vault_dir, "werracle_health.py"))

# Generate SHA256 manifest
manifest_path = os.path.join(vault_dir, "MANIFEST_SHA256.txt")
cmd = f"cd {vault_dir} && sha256sum * > MANIFEST_SHA256.txt"
subprocess.run(cmd, shell=True, check=True)

# Set strict permissions 700 / 600
os.chmod(vault_dir, 0o700)
for root, dirs, files in os.walk(vault_dir):
    for f in files:
        os.chmod(os.path.join(root, f), 0o600)

print(f"Sealed vault v102 successfully created and locked (0700/0600): {vault_dir}")

# Update kasa_kayma
subprocess.run(["/opt/apps/answerr/venv/bin/python3", "/opt/apps/werracle/health/kasa_kayma.py"], check=True)
print("Updated kasa_kayma.json successfully.")
