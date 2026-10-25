import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

script = """
import sys
sys.path.insert(0, '/opt/apps/answerr/api')
import radar_auth

k1 = radar_auth.generate_api_key(tier='institutional', email='eval@steakhouse.financial', days=30)
k2 = radar_auth.generate_api_key(tier='institutional', email='eval@gauntlet.xyz', days=30)
k3 = radar_auth.generate_api_key(tier='institutional', email='eval@re7.capital', days=30)

print(f"STEAKHOUSE_KEY={k1['api_key']}")
print(f"GAUNTLET_KEY={k2['api_key']}")
print(f"RE7_KEY={k3['api_key']}")
"""

sftp = ssh.open_sftp()
with sftp.open("/tmp/gen_curator_keys.py", "w") as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("python3 /tmp/gen_curator_keys.py && rm -f /tmp/gen_curator_keys.py")
output = stdout.read().decode()
print("Generated Keys:")
print(output)
print("Stderr:", stderr.read().decode())

# Sync hot backup
stdin, stdout, stderr = ssh.exec_command("/usr/local/bin/werracle-radar-db-backup.sh")
print("Hot backup sync:", stdout.read().decode().strip())

ssh.close()
