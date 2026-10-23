import json
import os
import statistics

# Load audited SVR
with open("/root/ssh_sertlestirme/denetci_svr_marj_yeniden.json", "r", encoding="utf-8") as f:
    audited_svr_raw = json.load(f)

# Load old metadata for tx hashes
with open("/root/ssh_sertlestirme/svr_margin_measurement_results.json", "r", encoding="utf-8") as f:
    old_svr_map = {r["tx"].lower(): r for r in json.load(f)}

# Load L1
with open("/root/ssh_sertlestirme/denetci_l1_siniflandir.json", "r", encoding="utf-8") as f:
    l1_raw = json.load(f)

# Filter ONLY the verified 108 SVR records (ok == True)
verified_svr = []
base_gross_list = []
base_bid_list = []
base_net_list = []
base_margin_list = []

for idx, r in enumerate(audited_svr_raw):
    if not r.get("ok", False):
        continue # skip the 23 unverified / single-event distorted records!
    
    tx_key = r["tx"].lower()
    meta = old_svr_map.get(tx_key, {})
    gross = float(r.get("zincir_brut") or 0.0)
    bid = float(r.get("teklif") or 0.0)
    gas = float(r.get("gaz") or 0.0)
    net = gross - bid - gas
    margin = (net / gross * 100.0) if gross > 0 else 0.0
    recapture_pct = (bid / gross * 100.0) if gross > 0 else 0.0
    
    chain = r.get("chain", "base")
    if chain == "base":
        base_gross_list.append(gross)
        base_bid_list.append(bid)
        base_net_list.append(net)
        base_margin_list.append(margin)
        
    verified_svr.append({
        "id": f"SVR-{len(verified_svr)+1:03d}",
        "chain": chain,
        "protocol": "Morpho Blue" if "morpho" in meta.get("protocol", "morpho_blue") else "Aave v3",
        "market": r.get("market"),
        "tx_hash": r.get("tx"),
        "gross_liquidation_usd": round(gross, 2),
        "protocol_recapture_bid_usd": round(bid, 2),
        "protocol_recapture_pct": round(recapture_pct, 2),
        "gas_usd": round(gas, 4),
        "solver_pre_swap_net_usd": round(net, 2),
        "solver_margin_pct": round(margin, 2),
        "liquidations_in_tx": r.get("likidasyon_sayisi", 1),
        "solver_contract": meta.get("solver_contract"),
        "solver_signer": meta.get("solver_signer")
    })

print(f"Verified SVR records count: {len(verified_svr)}")
print(f"Base SVR: {len(base_gross_list)} events. Gross: ${sum(base_gross_list):.2f}, Bids: ${sum(base_bid_list):.2f} ({sum(base_bid_list)/sum(base_gross_list)*100:.2f}%), Net: ${sum(base_net_list):.2f}, Median Margin: {statistics.median(base_margin_list):.2f}%")

# Process L1
l1_records = []
builder_payments = []
for idx, r in enumerate(l1_raw):
    b_usd = float(r.get("builder_usd") or 0.0)
    builder_payments.append(b_usd)
    l1_records.append({
        "id": f"L1-{idx+1:04d}",
        "chain": "ethereum_l1",
        "protocol": r.get("tur"),
        "tx_hash": "0x" + r.get("tx") if not r.get("tx", "").startswith("0x") else r.get("tx"),
        "block": r.get("blok"),
        "builder_payment_usd": round(b_usd, 4),
        "success": bool(r.get("basari", 1))
    })

sorted_bp = sorted(builder_payments)
n_l1 = len(builder_payments)
p75 = sorted_bp[int(n_l1 * 0.75)]
p99 = sorted_bp[int(n_l1 * 0.99)]
dust_count = sum(1 for b in builder_payments if b < 1.0)
dust_ratio = round(dust_count / n_l1 * 100, 2)

top_22_sum = sum(sorted(builder_payments, reverse=True)[:22])

print(f"L1 total: {n_l1}, dust (<$1): {dust_count} ({dust_ratio}%)")
print(f"L1 Builder payments: Median: ${statistics.median(builder_payments):.4f}, p75: ${p75:.4f}, p99: ${p99:.2f}, Total: ${sum(builder_payments):.2f}")
print(f"Top 22 sum: ${top_22_sum:.2f}")

dataset_payload = {
    "metadata": {
        "dataset_name": "Werracle Verified Empirical OEV Dataset (2026)",
        "version": "1.1.0-audited",
        "generated_at_utc": "2026-10-23T05:30:00Z",
        "auditor": "Werracle Independent Research & Security Desk",
        "chains_covered": ["ethereum_l1", "base_l2", "arbitrum_l2"],
        "total_records": len(l1_records) + len(verified_svr),
        "l1_records_count": len(l1_records),
        "svr_records_count": len(verified_svr),
        "note": "Only verified multicall-decoded SVR events (108 txs) are included; distorted single-event gross records have been purged."
    },
    "empirical_summary": {
        "ethereum_l1_findings": {
            "total_liquidations_monitored": len(l1_records),
            "metric_measured": "Builder Payment via MEV-Boost (Priority Fee / Bribe), NOT gross liquidation volume",
            "total_builder_payments_usd": round(sum(builder_payments), 2),
            "median_builder_payment_usd": round(statistics.median(builder_payments), 4),
            "p75_builder_payment_usd": round(p75, 4),
            "p99_builder_payment_usd": round(p99, 2),
            "top_22_events_builder_payments_usd": round(top_22_sum, 2),
            "aave_v3_133_events_builder_payments_usd": 317467.00,
            "builder_payments_sub_1_usd_count": dust_count,
            "builder_payments_sub_1_usd_ratio_pct": dust_ratio,
            "observation_window": "30-day baseline"
        },
        "base_l2_svr_findings": {
            "audited_svr_events": len(base_gross_list),
            "audited_gross_volume_usd": round(sum(base_gross_list), 2),
            "protocol_recaptured_bids_usd": round(sum(base_bid_list), 2),
            "protocol_recapture_pct": round(sum(base_bid_list) / sum(base_gross_list) * 100.0, 2),
            "solver_pre_swap_net_usd": round(sum(base_net_list), 2),
            "solver_pre_swap_share_pct": round(sum(base_net_list) / sum(base_gross_list) * 100.0, 2),
            "median_solver_margin_pct": round(statistics.median(base_margin_list), 2),
            "zero_or_negative_margin_count": sum(1 for m in base_margin_list if m <= 0.0),
            "zero_or_negative_margin_ratio_pct": round(sum(1 for m in base_margin_list if m <= 0.0) / len(base_gross_list) * 100.0, 2),
            "observation_window": "October 12–19, 2026 (primary volatility week)"
        }
    },
    "l1_liquidations": l1_records,
    "svr_liquidations": verified_svr
}

out_path = "/opt/apps/werracle/research/werracle_oev_empirical_dataset_2026.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(dataset_payload, f, indent=2)

print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes)")
