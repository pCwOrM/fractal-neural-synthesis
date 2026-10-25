import json, urllib.request

with open("/var/lib/werracle-health/morpho_golge/pazarlar.json") as f:
    pazarlar_data = json.load(f)

pazarlar = pazarlar_data.get("pazarlar", [])
market_keys = [("0x" + p["id"]) if not p["id"].startswith("0x") else p["id"] for p in pazarlar]

query = """
query($keys: [String!]) {
  markets(first: 100, where: { uniqueKey_in: $keys, chainId_in: [8453] }) {
    items {
      marketId
      listed
      warnings {
        type
        level
      }
      loanAsset {
        symbol
        address
      }
      collateralAsset {
        symbol
        address
      }
      state {
        borrowAssetsUsd
        supplyAssetsUsd
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://blue-api.morpho.org/graphql",
    data=json.dumps({"query": query, "variables": {"keys": market_keys}}).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "WerracleMarketAuditor/1.0"}
)

with urllib.request.urlopen(req, timeout=15) as resp:
    res = json.loads(resp.read().decode())
    items = res.get("data", {}).get("markets", {}).get("items", [])

print(f"Total monitored markets queried: {len(items)}")

listed = []
unlisted_or_warned = []

for it in items:
    mid = it["marketId"].lower()
    st = it.get("state") or {}
    b_usd = st.get("borrowAssetsUsd") or 0.0
    is_listed = it.get("listed", False)
    warns = it.get("warnings") or []
    lsym = (it.get("loanAsset") or {}).get("symbol", "N/A")
    csym = (it.get("collateralAsset") or {}).get("symbol", "N/A")
    
    # Check if flagged/warned or unlisted
    has_bad_warn = any(w.get("level") in ("RED", "YELLOW") or "UNRECOGNIZED" in w.get("type", "") for w in warns)
    is_test_token = any(x in f"{lsym}_{csym}".upper() for x in ("TEST", "HERMES", "FUSD", "KTA", "RLP", "MOCK"))
    
    if is_listed and not has_bad_warn and not is_test_token:
        listed.append((mid, f"{csym}/{lsym}", b_usd, warns))
    else:
        unlisted_or_warned.append((mid, f"{csym}/{lsym}", b_usd, is_listed, warns))

tot_clean = sum(x[2] for x in listed)
tot_flagged = sum(x[2] for x in unlisted_or_warned)

print(f"Clean / Listed markets: {len(listed)} markets, Total Borrow: ${tot_clean:,.2f}")
print(f"Flagged / Unlisted / Test markets: {len(unlisted_or_warned)} markets, Total Borrow: ${tot_flagged:,.2f}")
print(f"Grand Total: ${tot_clean + tot_flagged:,.2f}")

print("\n--- Sample Flagged Markets (top 10 by borrow) ---")
unlisted_or_warned.sort(key=lambda x: x[2], reverse=True)
for x in unlisted_or_warned[:10]:
    print(f"Pair: {x[1]} | Borrow: ${x[2]:,.2f} | Listed: {x[3]} | Warnings: {[w['type'] for w in x[4]]}")
