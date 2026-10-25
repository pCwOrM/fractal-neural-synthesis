"""
mechsrv Hot Backup Daemon for Werracle B2B DaaS API Database
Fetches /var/lib/werracle-health/werracle_api_keys.db from pcworm-root (207.180.255.35)
and stores dated hot backups in /home/pcworm/werracle_backups/
"""

import os
import sys
import time
import shutil
import urllib.request
import json
import sqlite3

BACKUP_DIR = "/home/pcworm/werracle_backups"
LOCAL_DB = os.path.join(BACKUP_DIR, "werracle_api_keys_replica.db")

def check_radar_health():
    url = "https://api.werracle.com/v1/radar/overview"
    req = urllib.request.Request(url, headers={"User-Agent": "WerracleMechsrvMonitor/2.0"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HEALTH OK: {url} responded in {elapsed_ms}ms (Status: {data.get('status')})")
                return True
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HEALTH ALERT: {url} failed: {e}")
        return False
    return False

if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    check_radar_health()
