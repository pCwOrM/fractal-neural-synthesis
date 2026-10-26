"""
Werracle B2B DaaS Authentication, Multi-Pay Checkout & Key Management Module
Handles API Key issuance, SHA-256 hashing, SQLite storage, sliding window rate limiting,
Multi-Chain Crypto verification (Base USDC, TRON TRC20 USDT, Ethereum/Arbitrum/BSC USDT & USDC,
Binance SAPI Deposit History reconciliation), and iyzico 3D Secure Credit Card checkout.
"""

import os
import time
import json
import hmac
import base64
import secrets
import hashlib
import sqlite3
import urllib.parse
import urllib.request
import urllib.error
import requests
from typing import Optional, Dict, Any, List

DB_PATH = "/var/lib/werracle-health/werracle_api_keys.db"
CONFIG_PATH = "/opt/apps/answerr/api/radar_b2b_config.json"

DEFAULT_CONFIG = {
    "usdc_deposit_address": "0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7",
    "trc20_usdt_deposit_address": "TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu",
    "payments_enabled": True,
    "max_payment_age_days": 7,
    "usdc_contract_base": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    "usdt_contract_tron": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
    "network": "base_mainnet",
    "chain_id": 8453,
    "base_rpcs": [
        "https://mainnet.base.org",
        "https://base-rpc.publicnode.com"
    ],
    "evm_networks": {
        "base": {
            "name": "Base Mainnet",
            "chain_id": 8453,
            "rpcs": ["https://mainnet.base.org", "https://base-rpc.publicnode.com"],
            "tokens": {
                "USDC": {"address": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", "decimals": 6},
                "USDT": {"address": "0xfde4c96c8593536e31f229ea8f37b2ada2699bb2", "decimals": 6}
            }
        },
        "ethereum": {
            "name": "Ethereum Mainnet (ERC20)",
            "chain_id": 1,
            "rpcs": ["https://ethereum-rpc.publicnode.com", "https://rpc.ankr.com/eth"],
            "tokens": {
                "USDC": {"address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "decimals": 6},
                "USDT": {"address": "0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals": 6}
            }
        },
        "arbitrum": {
            "name": "Arbitrum One",
            "chain_id": 42161,
            "rpcs": ["https://arb1.arbitrum.io/rpc", "https://arbitrum-one-rpc.publicnode.com"],
            "tokens": {
                "USDC": {"address": "0xaf88d065e77c8cc2239327c5edb3a432268e5831", "decimals": 6},
                "USDT": {"address": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", "decimals": 6}
            }
        },
        "bsc": {
            "name": "BNB Smart Chain (BEP20)",
            "chain_id": 56,
            "rpcs": ["https://bsc-dataseed.binance.org", "https://bsc-rpc.publicnode.com"],
            "tokens": {
                "USDC": {"address": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d", "decimals": 18},
                "USDT": {"address": "0x55d398326f99059ff775485246999027b3197955", "decimals": 18}
            }
        }
    },
    "pricing": {
        "pro": {
            "name": "Pro Researcher & Searcher",
            "amount_usdc": 149.0,
            "amount_try_net": 5190.0,
            "amount_try_vat": 1038.0,
            "amount_try_total": 6228.0,
            "duration_days": 30,
            "rate_limit_per_min": 600
        },
        "institutional": {
            "name": "Institutional Risk Curator",
            "amount_usdc": 499.0,
            "amount_try_net": 17390.0,
            "amount_try_vat": 3478.0,
            "amount_try_total": 20868.0,
            "duration_days": 30,
            "rate_limit_per_min": 3000
        }
    }
}

# In-memory validation cache (TTL 60s)
_KEY_CACHE: Dict[str, Dict[str, Any]] = {}
_CACHE_EXPIRY: Dict[str, float] = {}
_RATE_LIMIT_COUNTERS: Dict[str, Dict[int, int]] = {}


def load_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                merged = {**DEFAULT_CONFIG, **cfg}
                for t_k, t_v in DEFAULT_CONFIG["pricing"].items():
                    if t_k in merged.get("pricing", {}):
                        merged["pricing"][t_k] = {**t_v, **merged["pricing"][t_k]}
                return merged
        except Exception:
            pass
    return {**DEFAULT_CONFIG, "payments_enabled": False}


def claim_message(tx_hash: str, tier: str, email: str) -> str:
    """Exact text the payer signs (EIP-191 personal_sign) to bind a self-custody payment to this claim."""
    return ("Werracle Radar API key claim\n"
            f"tx: {tx_hash.strip().lower()}\n"
            f"tier: {tier.strip().lower()}\n"
            f"email: {(email or '').strip().lower()}")


def _rpc(rpcs, method, params):
    for rpc in rpcs:
        try:
            r = requests.post(rpc, json={"jsonrpc": "2.0", "method": method, "params": params, "id": 1},
                              headers={"User-Agent": "WerracleRadar/2.2"}, timeout=8)
            data = r.json()
            if data.get("result") is not None:
                return data["result"]
        except Exception:
            continue
    return None


def _signature_matches(payer: str, message: str, signature: str, rpcs) -> bool:
    """EOA (ecrecover) or smart-contract wallet (EIP-1271 isValidSignature)."""
    try:
        from eth_account import Account
        from eth_account.messages import encode_defunct
        if Account.recover_message(encode_defunct(text=message), signature=signature).lower() == payer.lower():
            return True
    except Exception:
        pass
    try:  # EIP-1271
        from eth_account.messages import _hash_eip191_message, encode_defunct
        h = _hash_eip191_message(encode_defunct(text=message)).hex().removeprefix("0x")
        sig = signature.lower().removeprefix("0x")
        data = ("0x1626ba7e" + h.rjust(64, "0") + "40".rjust(64, "0") + hex(len(sig) // 2)[2:].rjust(64, "0")
                + sig.ljust(((len(sig) + 63) // 64) * 64, "0"))
        res = _rpc(rpcs, "eth_call", [{"to": payer, "data": data}, "latest"])
        return bool(res) and res.lower().startswith("0x1626ba7e")
    except Exception:
        return False


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
                network TEXT DEFAULT 'base_mainnet',
                currency TEXT DEFAULT 'USDC',
                payment_method TEXT DEFAULT 'On-Chain Crypto',
                billing_json TEXT DEFAULT '{}',
                invoice_no TEXT DEFAULT '',
                key_prefix TEXT DEFAULT '',
                raw_api_key TEXT DEFAULT '',
                FOREIGN KEY (key_hash) REFERENCES api_keys(key_hash)
            );
        """)
        # Safe alter table for existing DBs
        for col, ctype in [
            ("network", "TEXT DEFAULT 'base_mainnet'"),
            ("currency", "TEXT DEFAULT 'USDC'"),
            ("payment_method", "TEXT DEFAULT 'On-Chain Crypto'"),
            ("billing_json", "TEXT DEFAULT '{}'"),
            ("invoice_no", "TEXT DEFAULT ''"),
            ("key_prefix", "TEXT DEFAULT ''"),
            ("raw_api_key", "TEXT DEFAULT ''")
        ]:
            try:
                conn.execute(f"ALTER TABLE payments ADD COLUMN {col} {ctype};")
            except Exception:
                pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS card_checkouts (
                basket_id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                token TEXT DEFAULT '',
                tier TEXT NOT NULL,
                email TEXT NOT NULL,
                net_try REAL NOT NULL,
                vat_try REAL NOT NULL,
                total_try REAL NOT NULL,
                billing_json TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'initiated',
                created_at REAL NOT NULL,
                paid_at REAL,
                payment_id TEXT DEFAULT '',
                card_last4 TEXT DEFAULT '',
                key_hash TEXT DEFAULT '',
                raw_api_key TEXT DEFAULT '',
                invoice_no TEXT DEFAULT ''
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                key_hash TEXT NOT NULL,
                minute_bucket INTEGER NOT NULL,
                request_count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (key_hash, minute_bucket)
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_tier ON api_keys(tier);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_rate_limits_bucket ON rate_limits(minute_bucket);")
    conn.close()


# Ensure DB schema is initialized on import
try:
    init_db()
except Exception:
    pass


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
        "key_prefix": f"{prefix}{random_token[:6]}...{random_token[-4:]}",
        "tier": tier.lower(),
        "email": email,
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "expires_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(expires_at)),
        "expires_at": expires_at,
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

    cached = _KEY_CACHE.get(k_hash)
    if cached and now < _CACHE_EXPIRY.get(k_hash, 0):
        if cached["status"] == "active" and now < cached["expires_at"]:
            return cached
        return None

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


def check_rate_limit(key_hash: str, limit_per_min: int, db_path: str = DB_PATH) -> bool:
    now_min = int(time.time() // 60)
    try:
        conn = get_db_connection(db_path)
        with conn:
            cursor = conn.execute("""
                INSERT INTO rate_limits (key_hash, minute_bucket, request_count)
                VALUES (?, ?, 1)
                ON CONFLICT(key_hash, minute_bucket) DO UPDATE SET request_count = request_count + 1
                RETURNING request_count;
            """, (key_hash, now_min))
            row = cursor.fetchone()
            current_count = row[0] if row else 1
            if now_min % 5 == 0:
                conn.execute("DELETE FROM rate_limits WHERE minute_bucket < ?", (now_min - 5,))
        conn.close()
        return current_count <= limit_per_min
    except Exception:
        counters = _RATE_LIMIT_COUNTERS.setdefault(key_hash, {})
        old_buckets = [b for b in counters if b < now_min - 2]
        for b in old_buckets:
            del counters[b]
        current_count = counters.get(now_min, 0)
        if current_count >= limit_per_min:
            return False
        counters[now_min] = current_count + 1
        return True


def _check_binance_deposit_by_txid(cfg: Dict[str, Any], tx_hash: str, required_amount: float) -> Optional[Dict[str, Any]]:
    """Checks Binance SAPI deposit history for USDC or USDT matching tx_hash."""
    ak = cfg.get("binance_api_key")
    sk = cfg.get("binance_api_secret")
    if not ak or not sk:
        return None
    tx_clean = tx_hash.strip().lower().removeprefix("0x")
    for coin in ["USDC", "USDT"]:
        try:
            ts = int(time.time() * 1000)
            q = urllib.parse.urlencode({"coin": coin, "timestamp": ts, "recvWindow": 10000})
            sig = hmac.new(sk.encode("utf-8"), q.encode("utf-8"), hashlib.sha256).hexdigest()
            url = f"https://api.binance.com/sapi/v1/capital/deposit/hisrec?{q}&signature={sig}"
            req = urllib.request.Request(url, headers={"X-MBX-APIKEY": ak, "User-Agent": "WerracleRadar/2.2"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                deposits = json.loads(resp.read().decode())
                for dep in deposits:
                    d_tx = str(dep.get("txId", "")).strip().lower().removeprefix("0x")
                    # Sometimes Binance prefixes or suffixes internal info, check substring match on 64-hex
                    if tx_clean and len(tx_clean) >= 60 and tx_clean in d_tx:
                        amt = float(dep.get("amount", 0))
                        status = int(dep.get("status", 0))
                        if status in (1, 6) and amt >= required_amount - 1.0:  # allow $1 network fee tolerance on CEX withdrawals
                            return {
                                "verified": True,
                                "coin": coin,
                                "amount": amt,
                                "network": dep.get("network", "BINANCE"),
                                "payer": dep.get("sourceAddress") or "Binance Verified Deposit",
                                "binance_synced": 1
                            }
        except Exception:
            continue
    return None


def _verify_trc20_usdt_onchain(tx_hash: str, expected_recipient: str, required_amount: float, max_age_days: float = 7.0) -> Optional[Dict[str, Any]]:
    """Verifies a TRON TRC20 USDT transfer via TronGrid API."""
    tx_clean = tx_hash.strip().removeprefix("0x")
    if len(tx_clean) != 64:
        return None
    try:
        url = f"https://api.trongrid.io/v1/transactions/{tx_clean}/events"
        r = requests.get(url, headers={"User-Agent": "WerracleRadar/2.2"}, timeout=8)
        if r.status_code == 200:
            data = r.json()
            for ev in data.get("data", []):
                if ev.get("event_name") == "Transfer" and ev.get("contract_address") == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
                    blk_ts = float(ev.get("block_timestamp", 0)) / 1000.0
                    if blk_ts > 0 and (time.time() - blk_ts) > max_age_days * 86400.0:
                        continue
                    res = ev.get("result", {})
                    val = float(res.get("value", 0)) / 1e6
                    if val >= required_amount - 1.0:
                        return {
                            "verified": True,
                            "coin": "USDT",
                            "amount": val,
                            "network": "tron_trc20",
                            "payer": res.get("from", "TRON TRC20 Sender"),
                            "binance_synced": 0
                        }
    except Exception:
        pass
    return None


def verify_base_usdc_payment(
    tx_hash: str,
    target_tier: str,
    email: str = "",
    signature: str = "",
    network: str = "base",
    token: str = "USDC",
    billing: Optional[Dict[str, Any]] = None,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    init_db(db_path)
    tx_hash_raw = tx_hash.strip()
    net_key = (network or "base").strip().lower()
    if net_key in ("trc20", "tron", "trx"):
        tx_hash = tx_hash_raw.lower().removeprefix("0x")
        if len(tx_hash) != 64:
            return {"success": False, "error": "Invalid TRON TRC20 tx_hash format (must be 64 hex characters)."}
    else:
        tx_hash = tx_hash_raw.lower()
        if not tx_hash.startswith("0x") or len(tx_hash) != 66:
            return {"success": False, "error": "Invalid EVM tx_hash format (must be 0x followed by 64 hex characters)."}

    cfg = load_config()
    if not cfg.get("payments_enabled", True) or not cfg.get("usdc_deposit_address"):
        return {"success": False, "error": "Self-serve payments are currently disabled. Contact sales: contact@werracle.com"}

    target_tier = target_tier.lower()
    if target_tier not in cfg["pricing"]:
        return {"success": False, "error": "Invalid tier requested. Choose 'pro' or 'institutional'."}

    tier_info = cfg["pricing"][target_tier]
    required_usdc = float(tier_info["amount_usdc"])

    # 1. Replay prevention check
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE lower(tx_hash) = ?", (tx_hash.lower(),))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        ex_dict = dict(existing)
        inv_no = ex_dict.get("invoice_no") or f"INV-2026-{hashlib.sha256(tx_hash.encode()).hexdigest()[:8].upper()}"
        return {
            "success": False,
            "error": f"Transaction {tx_hash} has already been claimed for an API Key.",
            "invoice_no": inv_no,
            "invoice_pdf_url": f"https://radar.werracle.com/v1/radar/invoice/{tx_hash}.pdf"
        }

    verified_transfer = False
    payer_address = None
    transferred_usdc = 0.0
    settled_coin = (token or "USDC").upper()
    settled_network = net_key
    binance_synced = 0

    # 2A. Check TRON TRC20 if network is trc20/tron
    if net_key in ("trc20", "tron", "trx"):
        trc_res = _verify_trc20_usdt_onchain(tx_hash, cfg.get("trc20_usdt_deposit_address", ""), required_usdc, float(cfg.get("max_payment_age_days", 7)))
        if not trc_res:
            trc_res = _check_binance_deposit_by_txid(cfg, tx_hash, required_usdc)
        if not trc_res:
            conn.close()
            return {
                "success": False,
                "error": f"No confirmed TRC20 USDT deposit of >= {required_usdc} USDT found for tx {tx_hash} yet. Please wait 1-2 minutes for TRON confirmation and retry."
            }
        verified_transfer = True
        payer_address = trc_res["payer"]
        transferred_usdc = trc_res["amount"]
        settled_coin = trc_res["coin"]
        settled_network = "tron_trc20"
        binance_synced = trc_res.get("binance_synced", 0)
    else:
        # 2B. EVM Networks (base, ethereum, arbitrum, bsc)
        evm_nets = cfg.get("evm_networks", DEFAULT_CONFIG["evm_networks"])
        net_cfg = evm_nets.get(net_key, evm_nets["base"])
        rpcs = net_cfg.get("rpcs", cfg.get("base_rpcs", DEFAULT_CONFIG["base_rpcs"]))
        deposit_recipient = cfg["usdc_deposit_address"].lower()

        receipt = _rpc(rpcs, "eth_getTransactionReceipt", [tx_hash])
        if not receipt:
            # Fallback: check Binance deposit history directly
            bin_res = _check_binance_deposit_by_txid(cfg, tx_hash, required_usdc)
            if bin_res:
                verified_transfer = True
                payer_address = bin_res["payer"]
                transferred_usdc = bin_res["amount"]
                settled_coin = bin_res["coin"]
                settled_network = bin_res["network"]
                binance_synced = 1
            else:
                conn.close()
                return {"success": False, "error": f"Transaction receipt not found on {net_cfg['name']}. Ensure tx is confirmed."}
        else:
            if receipt.get("status") != "0x1":
                conn.close()
                return {"success": False, "error": "Transaction failed or reverted on-chain."}

            blk = _rpc(rpcs, "eth_getBlockByNumber", [receipt.get("blockNumber"), False])
            max_age = float(cfg.get("max_payment_age_days", 7)) * 86400.0
            if not blk or time.time() - int(blk["timestamp"], 16) > max_age:
                conn.close()
                return {"success": False, "error": f"Payment is older than {cfg.get('max_payment_age_days', 7)} days. Contact sales: contact@werracle.com"}

            TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
            accepted_tokens = net_cfg.get("tokens", {"USDC": {"address": cfg["usdc_contract_base"].lower(), "decimals": 6}})
            token_map = {v["address"].lower(): (k, v["decimals"]) for k, v in accepted_tokens.items()}

            for l in receipt.get("logs", []):
                contract_addr = l.get("address", "").lower()
                if contract_addr not in token_map:
                    continue
                t_sym, t_dec = token_map[contract_addr]
                topics = l.get("topics", [])
                if len(topics) >= 3 and topics[0].lower() == TRANSFER_TOPIC:
                    from_addr = "0x" + topics[1][-40:].lower()
                    to_addr = "0x" + topics[2][-40:].lower()
                    raw_val = int(l.get("data", "0x0"), 16)
                    val_usd = raw_val / (10 ** t_dec)
                    if to_addr == deposit_recipient and (payer_address is None or from_addr == payer_address):
                        payer_address = from_addr
                        transferred_usdc += val_usd
                        settled_coin = t_sym
                        settled_network = net_cfg["name"]
                        if transferred_usdc >= required_usdc - 1.0:
                            verified_transfer = True

            if not verified_transfer:
                conn.close()
                return {
                    "success": False,
                    "error": f"No matching USDC/USDT transfer of >= {required_usdc} found to deposit address {deposit_recipient}. Detected: {transferred_usdc:.2f}."
                }

            # Check signature OR Binance deposit match
            if signature:
                if not _signature_matches(payer_address, claim_message(tx_hash, target_tier, email), signature, rpcs):
                    conn.close()
                    return {
                        "success": False,
                        "error": "Signature does not match the paying address.",
                        "sign_this_message": claim_message(tx_hash, target_tier, email),
                        "payer_address": payer_address
                    }
            else:
                # Check if Binance SAPI already sees this deposit (allows exchange withdrawals without signature)
                bin_res = _check_binance_deposit_by_txid(cfg, tx_hash, required_usdc)
                if bin_res:
                    binance_synced = 1
                else:
                    conn.close()
                    return {
                        "success": False,
                        "error": "signature required",
                        "sign_this_message": claim_message(tx_hash, target_tier, email),
                        "payer_address": payer_address,
                        "how": "Sign the exact message with the wallet that sent the USDC/USDT (personal_sign / EIP-191) and resend with 'signature'."
                    }

    # 3. Generate and store API key + Invoice Metadata
    key_info = generate_api_key(tier=target_tier, email=email, days=30, db_path=db_path)
    now = time.time()
    inv_no = f"INV-{time.strftime('%Y', time.gmtime(now))}-{hashlib.sha256(tx_hash.encode()).hexdigest()[:8].upper()}"
    billing_str = json.dumps(billing or {}, ensure_ascii=False)

    with conn:
        conn.execute("""
            INSERT INTO payments (
                tx_hash, payer_address, amount_usdc, tier, claimed_at, key_hash, verified_on_chain, binance_synced,
                network, currency, payment_method, billing_json, invoice_no, key_prefix, raw_api_key
            ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_hash, payer_address, transferred_usdc, target_tier, now, key_info["key_hash"], binance_synced,
            settled_network, settled_coin, f"On-Chain Crypto ({settled_network})", billing_str, inv_no,
            key_info["key_prefix"], key_info["api_key"]
        ))
    conn.close()

    return {
        "success": True,
        "message": f"Payment of {transferred_usdc:.2f} {settled_coin} on {settled_network} verified successfully!",
        "tier": target_tier,
        "api_key": key_info["api_key"],
        "rate_limit_per_min": key_info["rate_limit_per_min"],
        "expires_at_utc": key_info["expires_at_utc"],
        "invoice_no": inv_no,
        "invoice_pdf_url": f"https://radar.werracle.com/v1/radar/invoice/{tx_hash}.pdf",
        "instructions": "Pass header 'X-API-Key: wrk_...' or 'Authorization: Bearer wrk_...' with your requests."
    }


# ==============================================================================
# IYZICO 3D SECURE CREDIT CARD CHECKOUT FOR RADAR.WERRACLE.COM
# ==============================================================================

def _iyzico_headers(api_key: str, secret_key: str, uri_path: str, body: str) -> Dict[str, str]:
    rnd = f"{int(time.time() * 1000)}{secrets.randbelow(10 ** 9)}"
    sig = hmac.new(secret_key.encode("utf-8"), (rnd + uri_path + body).encode("utf-8"), hashlib.sha256).hexdigest()
    token = base64.b64encode(f"apiKey:{api_key}&randomKey:{rnd}&signature:{sig}".encode("utf-8")).decode("utf-8")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "WerracleRadar-Billing/2.2",
        "Authorization": "IYZWSv2 " + token,
        "x-iyzi-rnd": rnd
    }


def _iyzico_post(cfg: Dict[str, Any], path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    iyz = cfg.get("iyzico", {})
    ak = iyz.get("api_key", "")
    sk = iyz.get("secret_key", "")
    base_url = iyz.get("base_url", "https://api.iyzipay.com").rstrip("/")
    if not ak or not sk:
        return {"status": "failure", "errorMessage": "iyzico merchant credentials not configured."}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    headers = _iyzico_headers(ak, sk, path, body)
    req = urllib.request.Request(base_url + path, data=body.encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"status": "failure", "errorMessage": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": "failure", "errorMessage": str(e)}


def init_iyzico_card_checkout(tier: str, billing: Dict[str, Any], client_ip: str = "127.0.0.1", locale: str = "tr", db_path: str = DB_PATH) -> Dict[str, Any]:
    init_db(db_path)
    cfg = load_config()
    tier = (tier or "pro").lower()
    if tier not in cfg["pricing"]:
        return {"success": False, "error": "Invalid tier. Choose 'pro' or 'institutional'."}

    p_info = cfg["pricing"][tier]
    net_try = float(p_info.get("amount_try_net", 5190.0 if tier == "pro" else 17390.0))
    vat_try = float(p_info.get("amount_try_vat", round(net_try * 0.20, 2)))
    total_try = float(p_info.get("amount_try_total", round(net_try + vat_try, 2)))
    total_str = f"{total_try:.2f}"

    email = (billing.get("email") or "").strip()
    legal_name = (billing.get("company") or billing.get("legal_name") or "").strip()
    contact_name = (billing.get("contact_name") or legal_name).strip()
    tax_id = (billing.get("tax_id") or "11111111111").strip()
    address = (billing.get("address") or "Çukurova Teknokent").strip()
    city = (billing.get("city") or "Adana").strip()
    country = (billing.get("country") or "Türkiye").strip()
    phone = "".join(ch for ch in (billing.get("phone") or "+908503115203") if ch.isdigit() or ch == "+")
    if not phone.startswith("+"):
        phone = "+90" + phone.lstrip("0")

    if not email or "@" not in email or not legal_name:
        return {"success": False, "error": "Please provide your Company/Full Name and Email address for the invoice."}

    parts = contact_name.split()
    first, last = (" ".join(parts[:-1]), parts[-1]) if len(parts) > 1 else (contact_name, "Customer")
    digits = "".join(ch for ch in tax_id if ch.isdigit())
    identity = digits if len(digits) == 11 else "11111111111"

    basket_id = f"WRK-{int(time.time())}-{secrets.token_hex(4).upper()}"
    conv_id = f"CONV-{basket_id}"
    item_name = f"Werracle B2B Risk Radar API — {p_info['name']} (30 Gün)"

    payload = {
        "locale": "en" if locale == "en" else "tr",
        "conversationId": conv_id,
        "price": total_str,
        "paidPrice": total_str,
        "currency": "TRY",
        "basketId": basket_id,
        "paymentGroup": "PRODUCT",
        "callbackUrl": "https://radar.werracle.com/v1/radar/auth/iyzico/callback",
        "enabledInstallments": [1],
        "buyer": {
            "id": basket_id,
            "name": first[:60],
            "surname": last[:60],
            "identityNumber": identity,
            "email": email[:100],
            "gsmNumber": phone[:20],
            "registrationAddress": address[:200],
            "city": city[:60],
            "country": country[:60],
            "ip": client_ip or "127.0.0.1"
        },
        "billingAddress": {
            "contactName": legal_name[:100],
            "address": address[:200],
            "city": city[:60],
            "country": country[:60]
        },
        "basketItems": [
            {
                "id": f"werracle_{tier}",
                "name": item_name[:100],
                "category1": "Yazılım",
                "category2": "B2B DaaS API Abonelik",
                "itemType": "VIRTUAL",
                "price": total_str
            }
        ]
    }

    res = _iyzico_post(cfg, "/payment/iyzipos/checkoutform/initialize/auth/ecom", payload)
    if res.get("status") != "success" or not res.get("token") or not res.get("paymentPageUrl"):
        return {
            "success": False,
            "error": f"iyzico payment initialization failed: {res.get('errorMessage') or 'unknown error'}"
        }

    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            INSERT INTO card_checkouts (
                basket_id, conversation_id, token, tier, email, net_try, vat_try, total_try, billing_json, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'initiated', ?)
        """, (
            basket_id, conv_id, res["token"], tier, email, net_try, vat_try, total_try,
            json.dumps(billing, ensure_ascii=False), time.time()
        ))
    conn.close()

    return {
        "success": True,
        "provider": "iyzico",
        "basket_id": basket_id,
        "payment_page_url": res["paymentPageUrl"],
        "net_try": net_try,
        "vat_try": vat_try,
        "total_try": total_try,
        "currency": "TRY"
    }


def settle_iyzico_card_callback(token: str, db_path: str = DB_PATH) -> Dict[str, Any]:
    init_db(db_path)
    token = (token or "").strip()
    if not token:
        return {"success": False, "error": "Missing token"}

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM card_checkouts WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": "Checkout session not found"}

    chk = dict(row)
    if chk["status"] == "paid":
        conn.close()
        return {
            "success": True,
            "already_paid": True,
            "basket_id": chk["basket_id"],
            "tier": chk["tier"],
            "api_key": chk["raw_api_key"],
            "invoice_no": chk["invoice_no"],
            "invoice_pdf_url": f"https://radar.werracle.com/v1/radar/invoice/{chk['basket_id']}.pdf"
        }

    cfg = load_config()
    res = _iyzico_post(cfg, "/payment/iyzipos/checkoutform/auth/ecom/detail", {
        "locale": "tr",
        "token": token,
        "conversationId": chk["conversation_id"]
    })

    if res.get("status") != "success" or (res.get("paymentStatus") or "").upper() != "SUCCESS":
        with conn:
            conn.execute("UPDATE card_checkouts SET status = 'failed' WHERE basket_id = ?", (chk["basket_id"],))
        conn.close()
        return {"success": False, "error": res.get("errorMessage") or "Card payment was not approved."}

    # Issue API key & record payment
    key_info = generate_api_key(tier=chk["tier"], email=chk["email"], days=30, db_path=db_path)
    now = time.time()
    inv_no = f"INV-{time.strftime('%Y', time.gmtime(now))}-{chk['basket_id'][-8:]}"
    pay_id = str(res.get("paymentId") or chk["basket_id"])
    last4 = str(res.get("lastFourDigits") or "****")

    with conn:
        conn.execute("""
            UPDATE card_checkouts
            SET status = 'paid', paid_at = ?, payment_id = ?, card_last4 = ?, key_hash = ?, raw_api_key = ?, invoice_no = ?
            WHERE basket_id = ?
        """, (now, pay_id, last4, key_info["key_hash"], key_info["api_key"], inv_no, chk["basket_id"]))

        conn.execute("""
            INSERT OR REPLACE INTO payments (
                tx_hash, payer_address, amount_usdc, tier, claimed_at, key_hash, verified_on_chain, binance_synced,
                network, currency, payment_method, billing_json, invoice_no, key_prefix, raw_api_key
            ) VALUES (?, ?, ?, ?, ?, ?, 1, 1, 'iyzico_card', 'TRY', ?, ?, ?, ?, ?)
        """, (
            chk["basket_id"], f"Card **** {last4} (iyzico #{pay_id})", chk["total_try"], chk["tier"], now,
            key_info["key_hash"], f"iyzico 3D Secure Card (**** {last4})", chk["billing_json"], inv_no,
            key_info["key_prefix"], key_info["api_key"]
        ))
    conn.close()

    return {
        "success": True,
        "basket_id": chk["basket_id"],
        "tier": chk["tier"],
        "email": chk["email"],
        "api_key": key_info["api_key"],
        "rate_limit_per_min": key_info["rate_limit_per_min"],
        "expires_at_utc": key_info["expires_at_utc"],
        "invoice_no": inv_no,
        "invoice_pdf_url": f"https://radar.werracle.com/v1/radar/invoice/{chk['basket_id']}.pdf"
    }


def get_payment_for_invoice(payment_ref: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    init_db(db_path)
    ref = (payment_ref or "").strip().removesuffix(".pdf")
    if ref.lower() == "sample":
        now = time.time()
        return {
            "tx_hash": "0x8f94e2c7d3b109a4e6c218d5b049f1a2c3d4e5f60718293a4b5c6d7e8f901234",
            "payer_address": "0x71C...89A (Verified Institutional Subscriber)",
            "amount_usdc": 149.00,
            "net_amount": 149.00,
            "vat_amount": 0.00,
            "tier": "pro",
            "claimed_at": now,
            "expires_at": now + 30 * 86400,
            "network": "Base Mainnet (Chain ID 8453)",
            "currency": "USDC",
            "payment_method": "On-Chain Crypto (Base Mainnet USDC)",
            "recipient_address": "0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7 (Base Treasury)",
            "invoice_no": f"INV-{time.strftime('%Y', time.gmtime(now))}-SAMPLE01",
            "key_prefix": "wrk_pro_live_sample***",
            "rate_limit_per_min": 600,
            "billing": {
                "company": "Sample Quantitative DeFi Fund Ltd.",
                "contact_name": "Risk & Treasury Operations Desk",
                "tax_id": "CHE-116.284.910",
                "address": "Bahnhofstrasse 42, 8001 Zürich, Switzerland",
                "email": "treasury@samplequantfund.io"
            }
        }

    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE lower(tx_hash) = ? OR lower(invoice_no) = ?", (ref.lower(), ref.lower()))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    p = dict(row)
    cursor.execute("SELECT * FROM api_keys WHERE key_hash = ?", (p["key_hash"],))
    k_row = cursor.fetchone()
    conn.close()

    k_dict = dict(k_row) if k_row else {}
    billing = {}
    try:
        billing = json.loads(p.get("billing_json") or "{}")
    except Exception:
        pass

    curr = p.get("currency") or "USDC"
    amt = float(p.get("amount_usdc") or 149.0)
    if curr == "TRY":
        net_amt = round(amt / 1.20, 2)
        vat_amt = round(amt - net_amt, 2)
        recip = "ITouch Bilişim Sistemleri Ltd. Şti. — iyzico Merchant #276514"
    else:
        net_amt = amt
        vat_amt = 0.0
        recip = (
            "TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu (TRON TRC20 Treasury)"
            if "trc20" in str(p.get("network", "")).lower()
            else "0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7 (EVM Treasury)"
        )

    return {
        "tx_hash": p["tx_hash"],
        "payer_address": p["payer_address"],
        "amount_usdc": amt,
        "net_amount": net_amt,
        "vat_amount": vat_amt,
        "tier": p["tier"],
        "claimed_at": p["claimed_at"],
        "expires_at": k_dict.get("expires_at") or (p["claimed_at"] + 30 * 86400),
        "email": k_dict.get("email") or billing.get("email") or "",
        "network": p.get("network") or "Base Mainnet",
        "currency": curr,
        "payment_method": p.get("payment_method") or "On-Chain Crypto",
        "recipient_address": recip,
        "invoice_no": p.get("invoice_no") or f"INV-2026-{hashlib.sha256(p['tx_hash'].encode()).hexdigest()[:8].upper()}",
        "key_prefix": p.get("key_prefix") or k_dict.get("key_prefix") or f"wrk_{p['tier'][:4]}_live_***",
        "rate_limit_per_min": k_dict.get("rate_limit_per_min") or (3000 if p["tier"] == "institutional" else 600),
        "billing": billing
    }
