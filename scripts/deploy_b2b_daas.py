import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

sftp = ssh.open_sftp()

print("1. Backing up existing radar_router.py on remote...")
ssh.exec_command("cp /opt/apps/answerr/api/radar_router.py /opt/apps/answerr/api/radar_router.py.bak_pre_b2b_daas")

print("2. Uploading radar_auth.py...")
sftp.put("scripts/radar_auth.py", "/opt/apps/answerr/api/radar_auth.py")

print("3. Uploading radar_b2b_config.json...")
sftp.put("scripts/radar_b2b_config.json", "/opt/apps/answerr/api/radar_b2b_config.json")

print("4. Uploading manage_radar_daas.py...")
sftp.put("scripts/manage_radar_daas.py", "/opt/apps/answerr/api/manage_radar_daas.py")

print("5. Uploading new radar_router.py...")
sftp.put("scripts/radar_router_enriched_b2b.py", "/opt/apps/answerr/api/radar_router.py")

sftp.close()

print("6. Initializing SQLite Database /var/lib/werracle-health/werracle_api_keys.db...")
init_cmd = """
/opt/apps/answerr/venv/bin/python -c "
import sys
sys.path.insert(0, '/opt/apps/answerr/api')
import radar_auth
radar_auth.init_db()
print('Database initialized successfully.')
"
"""
stdin, stdout, stderr = ssh.exec_command(init_cmd)
print("Init output:", stdout.read().decode())
print("Init error:", stderr.read().decode())

print("7. Testing router import in production venv...")
test_cmd = """
/opt/apps/answerr/venv/bin/python -c "
import sys
sys.path.insert(0, '/opt/apps/answerr/api')
from radar_router import radar_router
print('radar_router imported successfully! Routes count:', len(radar_router.routes))
for r in radar_router.routes:
    print('   Route:', r.path, r.methods)
"
"""
stdin, stdout, stderr = ssh.exec_command(test_cmd)
test_out = stdout.read().decode()
test_err = stderr.read().decode()
print("Import test output:\n", test_out)
if test_err:
    print("Import test error:\n", test_err)

if "radar_router imported successfully" in test_out:
    print("8. Router test passed! Restarting answerr-api.service...")
    stdin, stdout, stderr = ssh.exec_command("systemctl restart answerr-api.service")
    time.sleep(2)
    stdin, stdout, stderr = ssh.exec_command("systemctl is-active answerr-api.service")
    status = stdout.read().decode().strip()
    print("answerr-api service status:", status)
else:
    print("WARNING: Import test failed. Did NOT restart service.")

ssh.close()
