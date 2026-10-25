"""
Werracle B2B DaaS Risk Radar Management CLI
Admin tool to update payment addresses, issue manual API keys,
inspect subscribers, and check on-chain transaction verifications.
"""

import sys
import json
import argparse
import time
from typing import Optional

import radar_auth

def cmd_set_address(args):
    addr = args.address.strip()
    if not addr.startswith("0x") or len(addr) != 42:
        print(f"Error: Invalid EVM address format: '{addr}' (must be 0x followed by 40 hex chars)")
        sys.exit(1)
        
    cfg = radar_auth.load_config()
    old_addr = cfg.get("usdc_deposit_address")
    cfg["usdc_deposit_address"] = addr.lower()
    
    with open(radar_auth.CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        
    print(f"USDC Deposit Address updated successfully:")
    print(f"  Old Address: {old_addr}")
    print(f"  New Address: {addr.lower()}")


def cmd_issue_key(args):
    tier = args.tier.lower()
    days = int(args.days)
    email = args.email or "manual_admin@werracle.com"
    
    key_info = radar_auth.generate_api_key(tier=tier, email=email, days=days)
    print("=" * 60)
    print("API KEY ISSUED SUCCESSFULLY:")
    print(f"  API Key:             {key_info['api_key']}")
    print(f"  Tier:                {key_info['tier']}")
    print(f"  Email:               {key_info['email']}")
    print(f"  Rate Limit:          {key_info['rate_limit_per_min']} req/min")
    print(f"  Created At:          {key_info['created_at_utc']}")
    print(f"  Expires At:          {key_info['expires_at_utc']}")
    print("=" * 60)
    print("Keep this key safe! It will NOT be shown in plain text again.")


def cmd_list_keys(args):
    conn = radar_auth.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key_prefix, tier, email, created_at, expires_at, status, rate_limit_per_min, request_count FROM api_keys ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    now = time.time()
    print(f"\nTotal Registered API Keys: {len(rows)}")
    print("-" * 90)
    print(f"{'PREFIX':<20} {'TIER':<15} {'STATUS':<10} {'REQ/MIN':<8} {'EXPIRES (DAYS)':<15} {'EMAIL'}")
    print("-" * 90)
    for r in rows:
        exp_days = round((r['expires_at'] - now) / 86400.0, 1)
        exp_str = f"{exp_days}d" if exp_days > 0 else "EXPIRED"
        print(f"{r['key_prefix']+'...':<20} {r['tier']:<15} {r['status']:<10} {r['rate_limit_per_min']:<8} {exp_str:<15} {r['email'] or 'N/A'}")
    print("-" * 90)


def cmd_list_payments(args):
    conn = radar_auth.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tx_hash, payer_address, amount_usdc, tier, claimed_at FROM payments ORDER BY claimed_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\nTotal Verified Payments: {len(rows)}")
    print("-" * 90)
    print(f"{'TX HASH':<45} {'USDC':<8} {'TIER':<15} {'PAYER'}")
    print("-" * 90)
    for r in rows:
        print(f"{r['tx_hash'][:42]+'...':<45} ${r['amount_usdc']:<7.2f} {r['tier']:<15} {r['payer_address']}")
    print("-" * 90)


def main():
    parser = argparse.ArgumentParser(description="Werracle B2B DaaS Admin Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    p_addr = subparsers.add_parser("set-address", help="Set Binance Base USDC deposit address")
    p_addr.add_argument("address", help="0x... EVM address")
    
    p_issue = subparsers.add_parser("issue-key", help="Manually issue an API key")
    p_issue.add_argument("--tier", default="pro", choices=["pro", "institutional"], help="Subscription tier")
    p_issue.add_argument("--days", default=30, type=int, help="Validity duration in days")
    p_issue.add_argument("--email", default="", help="Client email")
    
    subparsers.add_parser("list-keys", help="List registered API keys")
    subparsers.add_parser("list-payments", help="List verified payments")
    
    args = parser.parse_args()
    if args.command == "set-address":
        cmd_set_address(args)
    elif args.command == "issue-key":
        cmd_issue_key(args)
    elif args.command == "list-keys":
        cmd_list_keys(args)
    elif args.command == "list-payments":
        cmd_list_payments(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
