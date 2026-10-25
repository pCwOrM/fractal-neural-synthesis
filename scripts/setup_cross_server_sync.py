import paramiko

# 1. Connect to pcworm-root and generate ed25519 key if not exists
ssh_pcworm = paramiko.SSHClient()
ssh_pcworm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_pcworm.connect("207.180.255.35", username="root")

stdin, stdout, stderr = ssh_pcworm.exec_command("test -f /root/.ssh/id_ed25519 || ssh-keygen -t ed25519 -f /root/.ssh/id_ed25519 -N ''")
stdout.channel.recv_exit_status()

stdin, stdout, stderr = ssh_pcworm.exec_command("cat /root/.ssh/id_ed25519.pub")
pubkey = stdout.read().decode().strip()
print("pcworm-root public key:", pubkey)

# 2. Connect to mechsrv and append pubkey to authorized_keys
ssh_mechsrv = paramiko.SSHClient()
ssh_mechsrv.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_mechsrv.connect("173.212.201.159", port=2222, username="pcworm", key_filename=r"C:\Setup\code\mechsrv\.ssh\id_rsa")

cmd = f'grep -q "{pubkey}" /home/pcworm/.ssh/authorized_keys || echo "{pubkey}" >> /home/pcworm/.ssh/authorized_keys'
stdin, stdout, stderr = ssh_mechsrv.exec_command(cmd)
stdout.channel.recv_exit_status()
print("Appended pcworm-root pubkey to mechsrv authorized_keys.")

# 3. Test SCP from pcworm-root to mechsrv
test_cmd = "scp -o StrictHostKeyChecking=no -P 2222 /var/lib/werracle-health/werracle_api_keys.db pcworm@173.212.201.159:/home/pcworm/werracle_backups/werracle_api_keys_replica.db"
stdin, stdout, stderr = ssh_pcworm.exec_command(test_cmd)
exit_code = stdout.channel.recv_exit_status()
print("SCP test exit code:", exit_code)
if exit_code == 0:
    print("SUCCESS: pcworm-root successfully synced werracle_api_keys.db to mechsrv!")
else:
    print("SCP Error:", stderr.read().decode())

# 4. Verify file on mechsrv
stdin, stdout, stderr = ssh_mechsrv.exec_command("ls -lh /home/pcworm/werracle_backups/")
print("mechsrv backup directory contents:")
print(stdout.read().decode())

ssh_pcworm.close()
ssh_mechsrv.close()
