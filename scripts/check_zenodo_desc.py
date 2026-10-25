import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

cmd = 'curl -s -H "Accept: application/json" https://zenodo.org/api/records/23642090'
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
ssh.close()

data = json.loads(out)
desc = data.get("metadata", {}).get("description", "")
print("Description preview (first 500 chars):")
print(desc[:500])
print("\nDescription ends with:")
print(desc[-300:])
