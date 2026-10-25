"""
Werracle B2B DaaS Authentication & Key Management Module
Handles API Key issuance, SHA-256 hashing, SQLite storage,
sliding window rate limiting, and Base RPC USDC payment verification.
"""

import os
import time
import json
import secrets
import hashlib
import sqlite3
import requests
from typing import Optional, Dict, Any, Tuple

DB_PATH = "/var/lib/werracle-health/werracle_api_keys.db"
CONFIG_PATH = "/opt/apps/answerr/api/radar_b2b_config.json"

DEFAULT_CONFIG = {
    "usdc_deposit_address": "0x40366a7b7440939caaaaeab2075782725fa50012",
    "usdc_contract_base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913".lower(),
    "network": "base_mainnet",
    "chain_id": 8453,
    "base_rpcs": [
        "https://mainnet.base.org",
        "https://base-rpc.publicnode.com"
    ],
    "pricing": {
        "pro": {
            "name": "Pro Researcher & Searcher",
            "amount_usdc": 149.0,
            "duration_days": 30,
            "rate_limit_per_min": 600
        },
        "institutional": {
            "name": "Institutional Risk Curator",
            "amount_usdc": 499.0,
            "duration_days": 30,
            "rate_limit_per_min": 3000
        }
    }
}

# In-memory validation cache (TTL 60s)
_KEY_CACHE: Dict[str, Dict[str, Any]] = {}
_CACHE_EXPIRY: Dict[str, float] = {}

# Sliding window rate limit counter: {key_hash: {minute_bucket: count}}
_RATE_LIMIT_COUNTERS: Dict[str, Dict[int, int]] = {}


def load_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return DEFAULT_CONFIG


def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_db(db_path: str = DB_PATH):
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash TEXT PRIMARY KEY,
                key_prefix TEXT NOT NULL,
                tier TEXT NOT NULL,
                email TEXT,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                rate_limit_per_min INTEGER NOT NULL,
                request_count INTEGER NOT NULL DEFAULT 0,
                last_used_at REAL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                tx_hash TEXT PRIMARY KEY,
                payer_address TEXT NOT NULL,
                amount_usdc REAL NOT NULL,
                tier TEXT NOT NULL,
                claimed_at REAL NOT NULL,
                key_hash TEXT NOT NULL,
                verified_on_chain INTEGER NOT NULL DEFAULT 1,
                binance_synced INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (key_hash) REFERENCES api_keys(key_hash)
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_tier ON api_keys(tier);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);")
    conn.close()


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.strip().encode("utf-8")).hexdigest()


def generate_api_key(tier: str = "pro", email: str = "", days: int = 30, db_path: str = DB_PATH) -> Dict[str, Any]:
    cfg = load_config()
    tier_info = cfg.get("pricing", {}).get(tier.lower(), cfg["pricing"]["pro"])
    
    prefix = f"wrk_{tier[:4]}_live_"
    random_token = secrets.token_hex(20)
    raw_key = f"{prefix}{random_token}"
    k_hash = hash_key(raw_key)
    
    now = time.time()
    expires_at = now + (days * 86400.0)
    rate_limit = tier_info.get("rate_limit_per_min", 600)
    
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            INSERT INTO api_keys (
                key_hash, key_prefix, tier, email, created_at, expires_at, status, rate_limit_per_min, request_count
            ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, 0)
        """, (k_hash, prefix, tier.lower(), email, now, expires_at, rate_limit))
    conn.close()
    
    # Pre-cache
    _KEY_CACHE[k_hash] = {
        "key_hash": k_hash,
        "tier": tier.lower(),
        "email": email,
        "expires_at": expires_at,
        "status": "active",
        "rate_limit_per_min": rate_limit
    }
    _CACHE_EXPIRY[k_hash] = now + 60.0
    
    return {
        "api_key": raw_key,
        "key_hash": k_hash,
        "tier": tier.lower(),
        "email": email,
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "expires_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(expires_at)),
        "rate_limit_per_min": rate_limit
    }


def authenticate_key(raw_key: Optional[str], db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    if not raw_key:
        return None
    raw_key = raw_key.strip()
    if raw_key.startswith("Bearer "):
        raw_key = raw_key[7:].strip()
    if not raw_key.startswith("wrk_"):
        return None
        
    k_hash = hash_key(raw_key)
    now = time.time()
    
    # Check memory cache
    cached = _KEY_CACHE.get(k_hash)
    if cached and now < _CACHE_EXPIRY.get(k_hash, 0):
        if cached["status"] == "active" and now < cached["expires_at"]:
            return cached
        return None
        
    # Check SQLite DB
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE key_hash = ?", (k_hash,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    data = dict(row)
    if data["status"] != "active" or now >= data["expires_at"]:
        return None
        
    # Update cache
    _KEY_CACHE[k_hash] = {
        "key_hash": k_hash,
        "tier": data["tier"],
        "email": data["email"],
        "expires_at": data["expires_at"],
        "status": data["status"],
        "rate_limit_per_min": data["rate_limit_per_min"]
    }
    _CACHE_EXPIRY[k_hash] = now + 60.0
    return _KEY_CACHE[k_hash]


def check_rate_limit(key_hash: str, limit_per_min: int) -> bool:
    now_min = int(time.time() // 60)
    counters = _RATE_LIMIT_COUNTERS.setdefault(key_hash, {})
    
    # Clean old buckets
    old_buckets = [b for b in counters if b < now_min - 2]
    for b in old_buckets:
        del counters[b]
        
    current_count = counters.get(now_min, 0)
    if current_count >= limit_per_min:
        return False
        
    counters[now_min] = current_count + 1
    return True


def verify_base_usdc_payment(tx_hash: str, target_tier: str, email: str = "", db_path: str = DB_PATH) -> Dict[str, Any]:
    tx_hash = tx_hash.strip().lower()
    if not tx_hash.startswith("0x") or len(tx_hash) != 66:
        return {"success": False, "error": "Invalid tx_hash format (must be 0x followed by 64 hex characters)."}
        
    cfg = load_config()
    target_tier = target_tier.lower()
    if target_tier not in cfg["pricing"]:
        return {"success": False, "error": f"Invalid tier requested. Choose 'pro' or 'institutional'."}
        
    tier_info = cfg["pricing"][target_tier]
    required_usdc = float(tier_info["amount_usdc"])
    deposit_recipient = cfg["usdc_deposit_address"].lower()
    usdc_contract = cfg["usdc_contract_base"].lower()
    
    # 1. Replay prevention check
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE tx_hash = ?", (tx_hash,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"success": False, "error": f"Transaction {tx_hash} has already been claimed for an API Key."}
        
    # 2. Query Base RPC for transaction receipt
    rpcs = cfg.get("base_rpcs", DEFAULT_CONFIG["base_rpcs"])
    receipt = None
    for rpc in rpcs:
        try:
            payload = {"jsonrpc": "2.0", "method": "eth_getTransactionReceipt", "params": [tx_hash], "id": 1}
            r = requests.post(rpc, json=payload, headers={"User-Agent": "WerracleRadar/2.0"}, timeout=5)
            data = r.json()
            if "result" in data and data["result"]:
                receipt = data["result"]
                break
        except Exception:
            continue
            
    if not receipt:
        conn.close()
        return {"success": False, "error": "Transaction receipt not found on Base mainnet. Ensure tx is confirmed."}
        
    if receipt.get("status") != "0x1":
        conn.close()
        return {"success": False, "error": "Transaction failed or reverted on-chain."}
        
    # 3. Inspect logs for ERC-20 Transfer to deposit_recipient
    TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    verified_transfer = False
    payer_address = None
    transferred_usdc = 0.0
    
    for l in receipt.get("logs", []):
        if l.get("address", "").lower() != usdc_contract:
            continue
        topics = l.get("topics", [])
        if len(topics) >= 3 and topics[0].lower() == TRANSFER_TOPIC:
            from_addr = "0x" + topics[1][-40:].lower()
            to_addr = "0x" + topics[2][-40:].lower()
            raw_val = int(l.get("data", "0x0"), 16)
            usdc_val = raw_val / 1e6
            
            # Check if recipient matches configured deposit address
            if to_addr == deposit_recipient:
                payer_address = from_addr
                transferred_usdc += usdc_val
                if transferred_usdc >= required_usdc:
                    verified_transfer = True
                    break
                    
    if not verified_transfer:
        conn.close()
        return {
            "success": False,
            "error": (
                f"No matching USDC transfer of >= {required_usdc} USDC found to deposit address {deposit_recipient}."
                f" Detected to deposit: {transferred_usdc:.2f} USDC."
            )
        }
        
    # 4. Generate and store API key
    key_info = generate_api_key(tier=target_tier, email=email, days=30, db_path=db_path)
    now = time.time()
    
    with conn:
        conn.execute("""
            INSERT INTO payments (
                tx_hash, payer_address, amount_usdc, tier, claimed_at, key_hash, verified_on_chain, binance_synced
            ) VALUES (?, ?, ?, ?, ?, ?, 1, 0)
        """, (tx_hash, payer_address, transferred_usdc, target_tier, now, key_info["key_hash"]))
    conn.close()
    
    return {
        "success": True,
        "message": f"Payment of {transferred_usdc:.2f} USDC on Base verified successfully!",
        "tier": target_tier,
        "api_key": key_info["api_key"],
        "rate_limit_per_min": key_info["rate_limit_per_min"],
        "expires_at_utc": key_info["expires_at_utc"],
        "instructions": "Pass header 'X-API-Key: wrk_...' or 'Authorization: Bearer wrk_...' with your requests."
    }
