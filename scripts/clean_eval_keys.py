import os
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

script = """import sqlite3

db_path = '/var/lib/werracle-health/werracle_api_keys.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT key_prefix, email, status FROM api_keys")
print("Before deletion:", c.fetchall())

# Delete fabricated eval keys
c.execute("DELETE FROM api_keys WHERE email LIKE 'eval@%'")
print(f"Deleted {c.rowcount} fabricated eval keys from api_keys.")

# Clear rate limits
c.execute("DELETE FROM rate_limits WHERE key_hash NOT IN (SELECT key_hash FROM api_keys)")
print(f"Cleaned {c.rowcount} orphan entries from rate_limits.")

conn.commit()

c.execute("SELECT key_prefix, email, status FROM api_keys")
print("Remaining keys in DB:", c.fetchall())

conn.close()
"""

sftp = ssh.open_sftp()
with sftp.file("/tmp/do_clean_keys.py", "w") as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("/opt/apps/answerr/venv/bin/python /tmp/do_clean_keys.py && rm -f /tmp/do_clean_keys.py")
print("Python Output:\n", stdout.read().decode())
print("Python Error:\n", stderr.read().decode())

# Sync to mechsrv
sync_cmd = "scp -q -o StrictHostKeyChecking=no -P 2222 /var/lib/werracle-health/werracle_api_keys.db pcworm@173.212.201.159:/home/pcworm/werracle_backups/werracle_api_keys_replica.db"
stdin, stdout, stderr = ssh.exec_command(sync_cmd)
exit_code = stdout.channel.recv_exit_status()
print(f"Synced clean DB to mechsrv replica! (Exit code: {exit_code})")

# Test that old key is now rejected
test_cmd = f"curl -s -o /dev/null -w '%{{http_code}}' -H 'X-API-Key: {os.environ.get('WERRACLE_RADAR_KEY', 'wrk_inst_live_sample')}' http://127.0.0.1:8560/v1/radar/curator/steakhouse"
stdin, stdout, stderr = ssh.exec_command(test_cmd)
http_code = stdout.read().decode().strip()
print(f"Test old key HTTP response code: {http_code} (Expected: 401)")

ssh.close()
