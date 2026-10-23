import os
import shutil
import subprocess

API_DIR = "/opt/apps/answerr/api"
ROUTER_SRC = "/root/radar_router.py"
ROUTER_DST = os.path.join(API_DIR, "radar_router.py")
SERVER_PY = os.path.join(API_DIR, "server.py")
SERVER_BAK = os.path.join(API_DIR, "server.py.bak_pre_radar_20261023")

print("--- Deploying Werracle OEV & HF Radar API ---")

# 1. Copy router
shutil.copy2(ROUTER_SRC, ROUTER_DST)
print(f"Installed router to {ROUTER_DST}")

# 2. Backup server.py
if not os.path.exists(SERVER_BAK):
    shutil.copy2(SERVER_PY, SERVER_BAK)
    print(f"Created backup at {SERVER_BAK}")

# 3. Check if radar_router already imported
with open(SERVER_PY, "r", encoding="utf-8") as f:
    server_content = f.read()

snippet = """
# --- WERRACLE OEV & HF RADAR API (ADIM 4) ---
try:
    from radar_router import radar_router
    app.include_router(radar_router)
    print("[AnswerrAPI] Loaded /v1/radar OEV & HF Liquidation Radar Router successfully.")
except Exception as _radar_err:
    print(f"[AnswerrAPI] Warning: radar_router failed to load: {_radar_err}")
"""

if "from radar_router import radar_router" not in server_content:
    with open(SERVER_PY, "a", encoding="utf-8") as f:
        f.write("\n" + snippet + "\n")
    print("Appended radar_router registration to server.py")
else:
    print("radar_router already registered in server.py")

# 4. Verify syntax
cmd = "/opt/apps/answerr/venv/bin/python3 -m py_compile " + ROUTER_DST + " " + SERVER_PY
subprocess.run(cmd, shell=True, check=True)
print("Syntax verification passed.")

# 5. Restart answerr-api.service
subprocess.run("systemctl restart answerr-api.service", shell=True, check=True)
print("Restarted answerr-api.service")
