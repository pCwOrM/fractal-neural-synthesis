#!/usr/bin/env python3
"""
Werracle Empirical OEV & Liquidation Research Replication Script
Companion verification suite for Zenodo Open Science Package

Verifies the mathematical and statistical invariants reported in:
"Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR
 and Structural Centralization on Ethereum L1"

Authors: Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı
Contributor: Bekirhan Dağlı (ITouch Systems)
License: CC-BY-4.0 / MIT
"""

import os
import sys
import json
from statistics import median
from collections import Counter, defaultdict

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "werracle_oev_empirical_dataset_2026.json")

def verify_dataset():
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        sys.exit(1)

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 80)
    print("WERRACLE EMPIRICAL RESEARCH REPLICATION & VERIFICATION SUITE")
    print("=" * 80)
    meta = data.get("metadata", {})
    print(f"Dataset Name:     {meta.get('dataset_name')}")
    print(f"Version:          {meta.get('version')}")
    print(f"Auditor:          {meta.get('auditor')}")
    print(f"Total Records:    {meta.get('total_records')}")
    print(f"Generated UTC:    {meta.get('generated_at_utc')}")
    print("-" * 80)

    # 1. Base L2 SVR Audit
    svr_records = [r for r in data.get("svr_liquidations", []) if r.get("chain") == "base"]
    print(f"\n[1/3] VERIFYING BASE L2 CHAINLINK SVR METRICS (N = {len(svr_records)} txs)")
    assert len(svr_records) == 105, f"Expected 105 Base SVR events, got {len(svr_records)}"

    gross_usd = sum(r["gross_liquidation_usd"] for r in svr_records)
    recaptured_usd = sum(r["protocol_recapture_bid_usd"] for r in svr_records)
    solver_net_usd = sum(r["solver_pre_swap_net_usd"] for r in svr_records)
    gas_usd = sum(r.get("gas_usd", 0) for r in svr_records)

    recapture_pct = (recaptured_usd / gross_usd) * 100
    solver_share_pct = (solver_net_usd / gross_usd) * 100
    gas_share_pct = (gas_usd / gross_usd) * 100

    margins = [r["solver_margin_pct"] for r in svr_records]
    med_margin = median(margins)
    subzero_txs = [r for r in svr_records if r["solver_margin_pct"] <= 0.0]

    print(f"  • Gross Liquidation Value:      ${gross_usd:,.2f} USD")
    print(f"  • Protocol Recaptured Bids:     ${recaptured_usd:,.2f} USD ({recapture_pct:.2f}%)")
    print(f"  • Solver Pre-Swap Net Share:    ${solver_net_usd:,.2f} USD ({solver_share_pct:.2f}%)")
    print(f"  • L2 Gas Cost:                  ${gas_usd:,.2f} USD ({gas_share_pct:.2f}%)")
    print(f"  • Median Solver Margin:         {med_margin:.2f}%")
    print(f"  • Margin <= 0.00% Count:        {len(subzero_txs)} / {len(svr_records)} ({len(subzero_txs)/len(svr_records)*100:.1f}%)")

    # Invariant assertions
    assert abs(gross_usd - 190506.31) < 0.10, "Gross volume mismatch"
    assert abs(recaptured_usd - 186889.85) < 0.10, "Recapture bids mismatch"
    assert abs(recapture_pct - 98.10) < 0.05, "Recapture % mismatch"
    assert abs(med_margin - (-1.55)) < 0.05, "Median margin mismatch"
    assert len(subzero_txs) == 65, "Subzero tx count mismatch"
    print("  --> Base SVR Financial Invariants: [PASS]")

    # 2. Solver Decentralization & Multi-Call Bundling
    print(f"\n[2/3] VERIFYING SOLVER DECENTRALIZATION & MULTI-CALL PARSING")
    all_svr = data.get("svr_liquidations", [])
    all_solver_contracts = Counter(r.get("solver_contract") for r in all_svr)
    all_solver_signers = Counter(r.get("solver_signer") for r in all_svr)

    solver_contracts = Counter(r.get("solver_contract") for r in svr_records)
    solver_signers = Counter(r.get("solver_signer") for r in svr_records)
    multicalls = [r.get("liquidations_in_tx", 1) for r in svr_records]
    multi_txs = [c for c in multicalls if c > 1]
    max_subcalls = max(multicalls)

    print(f"  • Base Unique Solver Contracts: {len(solver_contracts)} (Total All Chains: {len(all_solver_contracts)})")
    print(f"  • Base Unique Signing EOAs:     {len(solver_signers)} (Total All Chains: {len(all_solver_signers)})")
    print(f"  • Multi-Call Bundled Txs:       {len(multi_txs)} / {len(multicalls)} ({len(multi_txs)/len(multicalls)*100:.2f}%)")
    print(f"  • Peak Sub-Calls in Single Tx:  {max_subcalls}")

    top_solver = solver_contracts.most_common(1)[0]
    top_solver_vol = sum(r["gross_liquidation_usd"] for r in svr_records if r.get("solver_contract") == top_solver[0])
    top_solver_share = (top_solver_vol / gross_usd) * 100
    print(f"  • Top Solver Count Share:       {top_solver[1]} txs ({top_solver[1]/len(svr_records)*100:.1f}%)")
    print(f"  • Top Solver Volume Share:      ${top_solver_vol:,.2f} ({top_solver_share:.2f}%) [Zero Monopoly]")

    assert len(solver_contracts) == 17, "Base solver contracts mismatch"
    assert len(all_solver_contracts) == 20, "Total solver contracts mismatch"
    assert len(solver_signers) == 24, "Base signer EOAs mismatch"
    assert len(all_solver_signers) == 27, "Total signer EOAs mismatch"
    assert len(multi_txs) == 68, "Multi-call tx count mismatch"
    assert max_subcalls == 32, "Peak subcalls mismatch"
    assert abs(top_solver_share - 31.64) < 0.10, "Top solver volume share mismatch"
    print("  --> Decentralization & Multi-Call Invariants: [PASS]")

    # 3. Ethereum L1 Builder Payments
    l1_records = data.get("l1_liquidations", [])
    print(f"\n[3/3] VERIFYING ETHEREUM L1 MEV-BOOST BUILDER PAYMENTS (N = {len(l1_records)} txs)")
    assert len(l1_records) == 1049, f"Expected 1,049 L1 events, got {len(l1_records)}"

    l1_payments = [r.get("builder_payment_usd", 0.0) for r in l1_records]
    total_l1_builder = sum(l1_payments)
    med_l1 = median(l1_payments)
    sub_1_usd = [p for p in l1_payments if p < 1.00]
    sorted_l1 = sorted(l1_payments, reverse=True)
    top_22_sum = sum(sorted_l1[:22])

    print(f"  • Total Builder Priority Fees:  ${total_l1_builder:,.2f} USD")
    print(f"  • Median Builder Payment:       ${med_l1:.2f} USD")
    print(f"  • Payments < $1.00 USD:         {len(sub_1_usd)} / {len(l1_records)} ({len(sub_1_usd)/len(l1_records)*100:.2f}%)")
    print(f"  • Top 22 Whale Txs Fees:        ${top_22_sum:,.2f} USD ({top_22_sum/total_l1_builder*100:.2f}%)")

    assert abs(total_l1_builder - 358316.62) < 1.0, "L1 total builder fee mismatch"
    assert len(sub_1_usd) == 848, "Sub-1 dollar count mismatch"
    assert abs(med_l1 - 0.08) < 0.02, "Median L1 builder fee mismatch"
    assert abs(top_22_sum - 344155.62) < 2.0, "Top 22 whale sum mismatch"
    print("  --> Ethereum L1 Power-Law Invariants: [PASS]")

    print("\n" + "=" * 80)
    print("ALL 15 MATHEMATICAL AND EMPIRICAL INVARIANTS CERTIFIED SUCCESSFULLY (100% PASS)")
    print("=" * 80)

if __name__ == "__main__":
    verify_dataset()
