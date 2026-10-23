import paramiko

host = "185.27.133.12"
port = 1394
user = "itouchsy"
password = "2HRaBof_pHdi{E}S"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port=port, username=user, password=password, timeout=15)
    
    cmds = [
        "ls -la /home/itouchsy/werracle.com",
        "head -n 30 /home/itouchsy/werracle.com/.htaccess 2>/dev/null",
        "cat /home/itouchsy/werracle.com/.htaccess 2>/dev/null"
    ]
    
    for c in cmds:
        print(f"\n--- COMMAND: {c} ---")
        stdin, stdout, stderr = client.exec_command(c)
        print(stdout.read().decode('utf-8', errors='ignore'))
        
    client.close()
except Exception as e:
    print(f"Error: {e}")
