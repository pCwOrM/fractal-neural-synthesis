import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

tests = [
    ("Local Overview", "curl -s http://127.0.0.1:8560/v1/radar/overview"),
    ("Local Plans", "curl -s http://127.0.0.1:8560/v1/radar/auth/plans"),
    ("Local Hot Positions (Free)", "curl -s http://127.0.0.1:8560/v1/radar/hot-positions"),
    ("Local Solvers (No Auth -> Expect 401)", "curl -s -w '\\nHTTP_CODE:%{http_code}' http://127.0.0.1:8560/v1/radar/solvers"),
    ("Local Curator (No Auth -> Expect 401)", "curl -s -w '\\nHTTP_CODE:%{http_code}' http://127.0.0.1:8560/v1/radar/curator/all"),
    ("Public Domain Overview", "curl -s https://api.werracle.com/v1/radar/overview"),
    ("Public Domain Plans", "curl -s https://api.werracle.com/v1/radar/auth/plans"),
]

for label, cmd in tests:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    print(f"\n=== {label} ===")
    try:
        data = json.loads(out)
        print(json.dumps(data, indent=2)[:300] + "...")
    except:
        print(out[:300])

ssh.close()
