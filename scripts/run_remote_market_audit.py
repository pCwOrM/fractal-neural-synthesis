import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

sftp = ssh.open_sftp()
sftp.put("scripts/audit_market_flags_remote.py", "/tmp/audit_market_flags.py")
sftp.close()

stdin, stdout, stderr = ssh.exec_command("python3 /tmp/audit_market_flags.py")
print("--- Remote Audit Output ---")
print(stdout.read().decode())
print("Stderr:", stderr.read().decode())

ssh.close()
