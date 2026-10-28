"""
Werracle B2B DaaS Risk Radar Management CLI
Admin tool to update payment addresses, issue manual API keys,
inspect subscribers, list/approve bank wire transfers, and check on-chain transaction verifications.
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
    print("-" * 105)
    print(f"{'PREFIX':<28} {'TIER':<15} {'EMAIL':<30} {'STATUS':<10} {'EXPIRES (DAYS)':<15}")
    print("-" * 105)
    for r in rows:
        exp_days = (r["expires_at"] - now) / 86400
        exp_str = f"{exp_days:.1f}d" if exp_days > 0 else "EXPIRED"
        email_str = r["email"] or "N/A"
        print(f"{r['key_prefix']:<28} {r['tier']:<15} {email_str[:28]:<30} {r['status']:<10} {exp_str:<15}")
    print("-" * 105)


def cmd_list_payments(args):
    conn = radar_auth.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tx_hash, amount_usdc, tier, payer_address, claimed_at FROM payments WHERE verified_on_chain = 1 ORDER BY claimed_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\nTotal Verified Payments: {len(rows)}")
    print("-" * 90)
    print(f"{'TX HASH':<45} {'USDC':<8} {'TIER':<15} {'PAYER'}")
    print("-" * 90)
    for r in rows:
        print(f"{r['tx_hash'][:42]+'...':<45} ${r['amount_usdc']:<7.2f} {r['tier']:<15} {r['payer_address']}")
    print("-" * 90)


def cmd_list_wires(args):
    conn = radar_auth.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tx_hash, payer_address, amount_usdc, currency, tier, claimed_at, 
               verified_on_chain, invoice_no, key_prefix, billing_json, raw_api_key
        FROM payments 
        WHERE network = 'bank_wire_teb' OR tx_hash LIKE 'WIRE-%'
        ORDER BY claimed_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    print(f"\nTotal Bank Wire Invoices: {len(rows)}")
    print("=" * 110)
    print(f"{'WIRE REF':<26} {'INVOICE':<16} {'AMOUNT':<12} {'STATUS':<10} {'BUYER / EMAIL'}")
    print("=" * 110)
    for r in rows:
        st = "PAID" if r["verified_on_chain"] else "PENDING"
        billing = {}
        try:
            billing = json.loads(r["billing_json"] or "{}")
        except Exception:
            pass
        buyer = billing.get("company") or r["payer_address"] or "-"
        em = billing.get("email") or ""
        amt_str = f"{r['amount_usdc']:.2f} {r['currency'] or 'USD'}"
        print(f"{r['tx_hash']:<26} {r['invoice_no']:<16} {amt_str:<12} {st:<10} {buyer} <{em}>")
    print("=" * 110)


def cmd_approve_wire(args):
    ref = args.ref.strip()
    conn = radar_auth.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE tx_hash = ? OR invoice_no = ?", (ref, ref))
    row = cursor.fetchone()
    if not row:
        print(f"Error: No bank wire record found for '{ref}'")
        conn.close()
        sys.exit(1)
        
    p = dict(row)
    if p.get("verified_on_chain"):
        print(f"Wire '{ref}' is ALREADY marked as PAID!")
        print(f"  Invoice: {p.get('invoice_no')}")
        print(f"  Key Prefix: {p.get('key_prefix')}")
        print(f"  API Key: {p.get('raw_api_key')}")
        conn.close()
        return

    billing = {}
    try:
        billing = json.loads(p.get("billing_json") or "{}")
    except Exception:
        pass

    email = billing.get("email") or "customer@werracle.com"
    tier = p.get("tier") or "pro"
    days = int(args.days or 30)

    # 1. Generate live key
    key_info = radar_auth.generate_api_key(tier=tier, email=email, days=days)
    api_key = key_info["api_key"]
    k_hash = key_info["key_hash"]
    k_prefix = key_info["key_prefix"]

    # 2. Update invoice number from PRO to INV
    old_inv = p.get("invoice_no") or ""
    new_inv = old_inv.replace("PRO-", "INV-") if "PRO-" in old_inv else old_inv

    with conn:
        conn.execute("""
            UPDATE payments
            SET verified_on_chain = 1,
                key_hash = ?,
                key_prefix = ?,
                raw_api_key = ?,
                invoice_no = ?
            WHERE tx_hash = ?
        """, (k_hash, k_prefix, api_key, new_inv, p["tx_hash"]))
    conn.close()

    print("=" * 70)
    print("SUCCESS: WIRE TRANSFER APPROVED & ACTIVATED")
    print("=" * 70)
    print(f"  Wire Reference:    {p['tx_hash']}")
    print(f"  Invoice No:        {new_inv}")
    print(f"  Buyer Email:       {email}")
    print(f"  Tier:              {tier}")
    print(f"  API Key:           {api_key}")
    print(f"  Expires At:        {key_info['expires_at_utc']}")
    print(f"  Invoice PDF:       https://radar.werracle.com/v1/radar/invoice/{p['tx_hash']}.pdf")
    print("=" * 70)


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
    subparsers.add_parser("list-wires", help="List all pending and verified bank wire transfers")

    p_app = subparsers.add_parser("approve-wire", help="Approve a pending bank wire transfer and activate API key")
    p_app.add_argument("ref", help="WIRE-... reference or PRO-... invoice number")
    p_app.add_argument("--days", default=30, type=int, help="Validity duration in days (default: 30)")

    args = parser.parse_args()
    if args.command == "set-address":
        cmd_set_address(args)
    elif args.command == "issue-key":
        cmd_issue_key(args)
    elif args.command == "list-keys":
        cmd_list_keys(args)
    elif args.command == "list-payments":
        cmd_list_payments(args)
    elif args.command == "list-wires":
        cmd_list_wires(args)
    elif args.command == "approve-wire":
        cmd_approve_wire(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
