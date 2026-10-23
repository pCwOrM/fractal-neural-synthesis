import paramiko
import sys

host = "185.27.133.12"
port = 1394
user = "itouchsy"
password = "2HRaBof_pHdi{E}S"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port=port, username=user, password=password, timeout=15)
    print("SSH connection successful!")
    
    # Check web server configuration & vhosts
    cmds = [
        "pwd; ls -la",
        "find ~ -maxdepth 3 -name '*werracle*' 2>/dev/null",
        "ls -la ~/public_html 2>/dev/null",
        "ls -la ~/domains 2>/dev/null",
        "ls -la /home/itouchsy/ 2>/dev/null"
    ]
    
    for c in cmds:
        print(f"\n--- COMMAND: {c} ---")
        stdin, stdout, stderr = client.exec_command(c)
        print(stdout.read().decode('utf-8', errors='ignore'))
        err = stderr.read().decode('utf-8', errors='ignore')
        if err:
            print("STDERR:", err)

    client.close()
except Exception as e:
    print(f"Error: {e}")
