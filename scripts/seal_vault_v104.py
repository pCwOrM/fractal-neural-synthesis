import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

seal_script = """
import os, shutil, time, sqlite3

tag = time.strftime("%Y%m%d_%H%M%S")
vname = f"v104_werracle_radar_daas_ve_svr_hibe_hazirlik_sealed_{tag}"
vdir = os.path.join("/opt/apps/werracle/sealed_vaults", vname)
os.makedirs(vdir, mode=0o700, exist_ok=True)

FILES = {
    "radar_router.py": "/opt/apps/answerr/api/radar_router.py",
    "radar_auth.py": "/opt/apps/answerr/api/radar_auth.py",
    "curator_stress.py": "/opt/apps/answerr/api/curator_stress.py",
    "radar_b2b_config.json": "/opt/apps/answerr/api/radar_b2b_config.json",
    "werracle_pazarlar_sync.py": "/usr/local/bin/werracle-pazarlar-sync.py",
    "werracle-radar-status.py": "/usr/local/bin/werracle-radar-status.py",
    "werracle-radar-db-backup.sh": "/usr/local/bin/werracle-radar-db-backup.sh",
    "cron_pazarlar": "/etc/cron.d/werracle-radar-pazarlar",
    "werracle_morpho_golge.py": "/opt/apps/werracle/health/werracle_morpho_golge.py",
    "werracle_l1_morpho.py": "/opt/apps/werracle/health/werracle_l1_morpho.py"
}

for name, path in FILES.items():
    if os.path.exists(path):
        dest = os.path.join(vdir, name)
        shutil.copy2(path, dest)
        os.chmod(dest, 0o600)

# Consistent SQLite backup of keys DB
src_db = "/var/lib/werracle-health/werracle_api_keys.db"
dest_db = os.path.join(vdir, "werracle_api_keys_sealed.db")
if os.path.exists(src_db):
    src_conn = sqlite3.connect(src_db)
    dest_conn = sqlite3.connect(dest_db)
    src_conn.backup(dest_conn)
    src_conn.close()
    dest_conn.close()
    os.chmod(dest_db, 0o600)

# Seal directory
os.chmod(vdir, 0o700)
print(f"Vault {vname} sealed successfully with {len(os.listdir(vdir))} items.")
"""

sftp = ssh.open_sftp()
with sftp.open("/tmp/seal_v104.py", "w") as f:
    f.write(seal_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("python3 /tmp/seal_v104.py && rm -f /tmp/seal_v104.py")
output = stdout.read().decode()
print(output)
print("Stderr:", stderr.read().decode())

# Hot backup sync
stdin, stdout, stderr = ssh.exec_command("/usr/local/bin/werracle-radar-db-backup.sh")
print("Hot backup sync to mechsrv:", stdout.read().decode().strip())

ssh.close()
