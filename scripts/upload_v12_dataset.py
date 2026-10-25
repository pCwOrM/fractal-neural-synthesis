import zipfile
import paramiko
import os

zip_path = r"C:\Setup\pcworm_server\oev_v2\replication_package_v2.zip"
with zipfile.ZipFile(zip_path) as z:
    dataset_bytes = z.read("oev_replication_package_v2/data/werracle_oev_empirical_dataset_2026_v1.2.json")
    print(f"Extracted dataset v1.2: {len(dataset_bytes)} bytes")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

sftp = ssh.open_sftp()
dest_path = "/opt/apps/werracle/research/werracle_oev_empirical_dataset_2026_v1.2.json"
with sftp.file(dest_path, "wb") as f:
    f.write(dataset_bytes)
print(f"Uploaded v1.2 dataset to remote: {dest_path}")

# Also update the symlink or default dataset path
stdin, stdout, stderr = ssh.exec_command(f"ls -lh {dest_path}")
print(stdout.read().decode())

sftp.close()
ssh.close()
