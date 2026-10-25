import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

# Issue a Pro Key
print("--- 1. Issuing Test Pro Key ---")
cmd = "/opt/apps/answerr/venv/bin/python /opt/apps/answerr/api/manage_radar_daas.py issue-key --tier pro --email test_searcher@werracle.com --days 30"
stdin, stdout, stderr = ssh.exec_command(cmd)
pro_out = stdout.read().decode()
print(pro_out)

pro_key = None
for line in pro_out.splitlines():
    if "API Key:" in line:
        pro_key = line.split("API Key:")[1].strip()

print(f"Captured Pro Key: {pro_key}")

# Issue an Institutional Key
print("\n--- 2. Issuing Test Institutional Key ---")
cmd = "/opt/apps/answerr/venv/bin/python /opt/apps/answerr/api/manage_radar_daas.py issue-key --tier institutional --email test_curator@steakhouse.financial --days 30"
stdin, stdout, stderr = ssh.exec_command(cmd)
inst_out = stdout.read().decode()
print(inst_out)

inst_key = None
for line in inst_out.splitlines():
    if "API Key:" in line:
        inst_key = line.split("API Key:")[1].strip()

print(f"Captured Institutional Key: {inst_key}")

# Test verify-key endpoint
print("\n--- 3. Testing /v1/radar/auth/verify-key with Pro Key ---")
cmd = f"curl -s -H 'X-API-Key: {pro_key}' http://127.0.0.1:8560/v1/radar/auth/verify-key"
stdin, stdout, stderr = ssh.exec_command(cmd)
print("Verify key response:", stdout.read().decode())

# Test Solvers with Pro Key
print("\n--- 4. Testing /v1/radar/solvers with Pro Key ---")
cmd = f"curl -s -H 'X-API-Key: {pro_key}' http://127.0.0.1:8560/v1/radar/solvers"
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
data = json.loads(out)
print(f"Solvers success! Total active solvers: {data.get('total_active_solvers')}")
if data.get('solvers_ranked'):
    print("Top solver 0:", json.dumps(data['solvers_ranked'][0], indent=2))

# Test Curator with Pro Key (should fail with 403 Forbidden because Curator requires Institutional)
print("\n--- 5. Testing /v1/radar/curator/all with Pro Key (Expect 403) ---")
cmd = f"curl -s -w '\\nHTTP_CODE:%{{http_code}}' -H 'X-API-Key: {pro_key}' http://127.0.0.1:8560/v1/radar/curator/all"
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())

# Test Curator with Institutional Key (should succeed with 200 OK)
print("\n--- 6. Testing /v1/radar/curator/all with Institutional Key (Expect 200) ---")
cmd = f"curl -s -H 'X-API-Key: {inst_key}' http://127.0.0.1:8560/v1/radar/curator/all"
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
data = json.loads(out)
print(f"Curator success! Vault risk score: {data.get('vault_risk_score')}, Status: {data.get('risk_status')}")
print("Stress test simulations:", json.dumps(data.get('stress_test_simulations'), indent=2))

ssh.close()
