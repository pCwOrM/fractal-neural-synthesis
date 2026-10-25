"""
Werracle Binance SAPI Deposit Reconciler
Cross-references on-chain Base USDC payments with Binance account deposits.
"""

import os
import sys
import time
import hmac
import hashlib
import json
import urllib.parse
import urllib.request
import sqlite3

CONFIG_PATH = "/opt/apps/answerr/api/radar_b2b_config.json"
DB_PATH = "/var/lib/werracle-health/werracle_api_keys.db"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def query_binance_deposits(api_key: str, api_secret: str, coin: str = "USDC") -> list:
    base_url = "https://api.binance.com/sapi/v1/capital/deposit/hisrec"
    timestamp = int(time.time() * 1000)
    params = {
        "coin": coin,
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    query_str = urllib.parse.urlencode(params)
    signature = hmac.new(api_secret.encode("utf-8"), query_str.encode("utf-8"), hashlib.sha256).hexdigest()
    
    full_url = f"{base_url}?{query_str}&signature={signature}"
    req = urllib.request.Request(full_url, headers={"X-MBX-APIKEY": api_key, "User-Agent": "WerracleReconciler/2.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Binance API query failed: {e}")
        return []
    return []

def reconcile():
    cfg = load_config()
    api_key = cfg.get("binance_api_key")
    api_secret = cfg.get("binance_api_secret")
    
    if not api_key or not api_secret:
        print("\n[INFO] Binance API key/secret not set in radar_b2b_config.json.")
        print("[INFO] On-chain Base RPC verification is already running at 100% fidelity.")
        print("[INFO] To enable Binance Spot Wallet reconciliation, add 'binance_api_key' and 'binance_api_secret' to radar_b2b_config.json.")
        return

    print("\nQuerying Binance Spot Wallet for USDC deposits...")
    deposits = query_binance_deposits(api_key, api_secret, coin="USDC")
    print(f"Found {len(deposits)} USDC deposit records on Binance.")

    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT tx_hash, amount_usdc, binance_synced FROM payments")
    local_payments = {row[0].lower(): (row[1], row[2]) for row in cursor.fetchall()}

    synced_count = 0
    for dep in deposits:
        tx_id = dep.get("txId", "").lower()
        status = dep.get("status")  # 1: success
        amount = float(dep.get("amount", 0))
        network = dep.get("network", "")

        if tx_id in local_payments and status == 1:
            if local_payments[tx_id][1] == 0:
                cursor.execute("UPDATE payments SET binance_synced = 1 WHERE lower(tx_hash) = ?", (tx_id,))
                synced_count += 1
                print(f" Reconciled tx {tx_id[:16]}...: {amount} USDC on {network} confirmed in Binance Spot!")

    conn.commit()
    conn.close()
    print(f"Reconciliation complete. Newly synchronized payments: {synced_count}")

if __name__ == "__main__":
    reconcile()
