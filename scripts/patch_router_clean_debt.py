with open("scripts/radar_router_remote.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update total_monitored_debt calculation
old_calc = """    pazarlar_data = _get_cached_json(MORPHO_PAZARLAR, {}).get("pazarlar", [])

    total_monitored_debt = sum(float(m.get("borc_usd", 0) or 0) for m in pazarlar_data)"""

new_calc = """    pazarlar_data = _get_cached_json(MORPHO_PAZARLAR, {}).get("pazarlar", [])

    # Separate verified listed markets from unlisted/spam markets
    clean_pazarlar = [m for m in pazarlar_data if m.get("listed", False) is True]
    active_pazarlar = clean_pazarlar if clean_pazarlar else pazarlar_data
    clean_debt_usd = round(sum(float(m.get("borc_usd", 0) or 0) for m in active_pazarlar), 2)
    raw_debt_usd = round(sum(float(m.get("borc_usd", 0) or 0) for m in pazarlar_data), 2)"""

assert old_calc in content, "old_calc target not found!"
content = content.replace(old_calc, new_calc)

# 2. Update realtime_surveillance dict
old_surv = """        "realtime_surveillance": {
            "base_l2": {
                "chain_id": 8453,
                "markets_monitored": len(pazarlar_data) or morpho_st.get("pazar"),
                "total_monitored_debt_usd": total_monitored_debt,
                "markets_debt_snapshot_utc": markets_snapshot_utc,"""

new_surv = """        "realtime_surveillance": {
            "base_l2": {
                "chain_id": 8453,
                "markets_monitored": len(active_pazarlar),
                "total_monitored_debt_usd": clean_debt_usd,
                "unlisted_markets_filtered": len(pazarlar_data) - len(active_pazarlar),
                "unlisted_raw_debt_usd": round(raw_debt_usd - clean_debt_usd, 2),
                "markets_debt_snapshot_utc": markets_snapshot_utc,"""

assert old_surv in content, "old_surv target not found!"
content = content.replace(old_surv, new_surv)

# 3. Update dashboard subtitle
old_dash = """                <div class="stat-sub">Across 83 Morpho Blue markets</div>"""
new_dash = """                <div class="stat-sub">Across 38 verified listed markets (45 unlisted filtered)</div>"""

assert old_dash in content, "old_dash target not found!"
content = content.replace(old_dash, new_dash)

# 4. Update Decision Speed label to clarify compute latency vs 200ms flashblocks
old_speed = """                <div class="stat-label">Reflex Decision Speed</div>
                <div class="stat-val">{overview['realtime_surveillance']['base_l2'].get('decision_compute_ms') or '—'} ms</div>
                <div class="stat-sub">Local decision compute latency</div>"""

new_speed = """                <div class="stat-label">Decision Compute Latency</div>
                <div class="stat-val">{overview['realtime_surveillance']['base_l2'].get('decision_compute_ms') or '—'} ms</div>
                <div class="stat-sub">Algorithmic compute over 200 ms flashblocks</div>"""

if old_speed in content:
    content = content.replace(old_speed, new_speed)

with open("scripts/radar_router_patched.py", "w", encoding="utf-8") as f:
    f.write(content)

print("scripts/radar_router_patched.py generated successfully.")
