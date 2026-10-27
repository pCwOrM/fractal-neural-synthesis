#!/usr/bin/env python3
"""
Werracle Dual-Chain Morpho Blue Market & TVL Sync (Base L2 chainId=8453 + Ethereum Mainnet chainId=1)
Updates /var/lib/werracle-health/morpho_golge/pazarlar.json and /var/lib/werracle-health/l1_morpho/pazarlar.json
with live borrowAssetsUsd, supplyAssetsUsd, asset prices, and official Morpho 'listed' (whitelisted) flags.
"""
import json
import os
import time
import urllib.request

GRAPHQL_URL = "https://blue-api.morpho.org/graphql"

CHAINS = [
    {
        "name": "Base L2",
        "chain_id": 8453,
        "pazarlar_path": "/var/lib/werracle-health/morpho_golge/pazarlar.json",
    },
    {
        "name": "Ethereum Mainnet",
        "chain_id": 1,
        "pazarlar_path": "/var/lib/werracle-health/l1_morpho/pazarlar.json",
    },
]

QUERY = """
query($chainId: Int!, $first: Int!, $skip: Int!) {
  markets(first: $first, skip: $skip, orderBy: BorrowAssetsUsd, orderDirection: Desc, where: { chainId_in: [$chainId] }) {
    items {
      marketId
      listed
      lltv
      loanAsset { address symbol decimals priceUsd }
      collateralAsset { address symbol decimals priceUsd }
      state {
        borrowAssetsUsd
        supplyAssetsUsd
        utilization
      }
    }
    pageInfo {
      countTotal
    }
  }
}
"""


def fetch_chain_markets(chain_id: int) -> dict:
    live_map = {}
    skip = 0
    batch = 500
    while True:
        payload = json.dumps({
            "query": QUERY,
            "variables": {"chainId": chain_id, "first": batch, "skip": skip}
        }).encode("utf-8")
        req = urllib.request.Request(
            GRAPHQL_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Werracle-Risk-Radar/2.2"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        m_block = (data.get("data") or {}).get("markets") or {}
        items = m_block.get("items") or []
        total = (m_block.get("pageInfo") or {}).get("countTotal") or 0
        for item in items:
            ukey = (item.get("marketId") or "").lower().replace("0x", "")
            state = item.get("state") or {}
            loan = item.get("loanAsset") or {}
            coll = item.get("collateralAsset") or {}
            live_map[ukey] = {
                "borc_usd": round(float(state.get("borrowAssetsUsd") or 0.0), 2),
                "arz_usd": round(float(state.get("supplyAssetsUsd") or 0.0), 2),
                "utilization": round(float(state.get("utilization") or 0.0), 4),
                "listed": bool(item.get("listed", False)),
                "loan_sym": loan.get("symbol"),
                "loan_usd": float(loan.get("priceUsd") or 0.0),
                "coll_sym": coll.get("symbol"),
                "coll_usd": float(coll.get("priceUsd") or 0.0),
            }
        skip += len(items)
        if not items or skip >= total or skip >= 2500:
            break
    return live_map


def sync_chain(cfg: dict):
    path = cfg["pazarlar_path"]
    chain_id = cfg["chain_id"]
    name = cfg["name"]
    if not os.path.exists(path):
        print(f"[WARN] {path} not found for {name}")
        return

    with open(path, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    live_map = fetch_chain_markets(chain_id)
    updated_count = 0
    clean_debt = 0.0
    raw_debt = 0.0
    clean_supply = 0.0
    listed_count = 0

    for m in local_data.get("pazarlar", []):
        mid = (m.get("id") or "").lower().replace("0x", "")
        if mid in live_map:
            info = live_map[mid]
            m["borc_usd"] = info["borc_usd"]
            m["arz_usd"] = info["arz_usd"]
            m["utilization"] = info["utilization"]
            m["listed"] = info["listed"]
            if info.get("loan_sym") and not m.get("loan_sym"):
                m["loan_sym"] = info["loan_sym"]
            if info.get("coll_sym") and not m.get("coll_sym"):
                m["coll_sym"] = info["coll_sym"]
            if info.get("loan_usd"):
                m["loan_usd"] = info["loan_usd"]
            if info.get("coll_usd"):
                m["coll_usd"] = info["coll_usd"]
            raw_debt += info["borc_usd"]
            if info["listed"]:
                clean_debt += info["borc_usd"]
                clean_supply += info["arz_usd"]
                listed_count += 1
            updated_count += 1

    # Sort listed markets first, then by borc_usd descending
    local_data["pazarlar"].sort(
        key=lambda x: (1 if x.get("listed", False) else 0, float(x.get("borc_usd", 0) or 0)),
        reverse=True
    )
    local_data["son_fiyat_senkron_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    local_data["chain_id"] = chain_id
    local_data["listed_markets_count"] = listed_count
    local_data["listed_debt_usd"] = round(clean_debt, 2)
    local_data["listed_supply_usd"] = round(clean_supply, 2)

    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(local_data, f, indent=1)
    os.chmod(tmp_path, 0o644)
    os.replace(tmp_path, path)
    print(
        f"[OK] {name} (chainId={chain_id}): Updated {updated_count}/{len(local_data.get('pazarlar', []))} markets | "
        f"Verified Listed ({listed_count}): Borrow=${clean_debt:,.2f}, Supply=${clean_supply:,.2f} (Raw Borrow: ${raw_debt:,.2f})"
    )


def main():
    for cfg in CHAINS:
        try:
            sync_chain(cfg)
        except Exception as e:
            print(f"[ERR] Failed syncing {cfg['name']}: {e}")


if __name__ == "__main__":
    main()
