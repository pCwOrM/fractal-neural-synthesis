import json
import urllib.request
import os
import sys
import time

MORPHO_API = "https://blue-api.morpho.org/graphql"
PAZARLAR_PATH = "/var/lib/werracle-health/morpho_golge/pazarlar.json"

def sync_markets(pazarlar_path=PAZARLAR_PATH):
    if not os.path.exists(pazarlar_path):
        print(f"Error: {pazarlar_path} does not exist.")
        return False
        
    with open(pazarlar_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    pazarlar = data.get("pazarlar", [])
    if not pazarlar:
        print("No markets found in pazarlar.json")
        return False
        
    # Map market id -> market obj
    market_keys = []
    key_to_pazar = {}
    for p in pazarlar:
        raw_id = p.get("id", "").strip().lower()
        if not raw_id:
            continue
        full_key = ("0x" + raw_id) if not raw_id.startswith("0x") else raw_id
        market_keys.append(full_key)
        key_to_pazar[full_key] = p
        
    print(f"Syncing {len(market_keys)} markets from Morpho Blue GraphQL...")
    
    query = """
    query($keys: [String!]) {
      markets(first: 100, where: { uniqueKey_in: $keys, chainId_in: [8453] }) {
        items {
          marketId
          state {
            borrowAssetsUsd
            supplyAssetsUsd
          }
        }
      }
    }
    """
    
    req = urllib.request.Request(
        MORPHO_API,
        data=json.dumps({"query": query, "variables": {"keys": market_keys}}).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "WerracleMarketUpdater/2.1"}
    )
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode())
        
    items = res.get("data", {}).get("markets", {}).get("items", [])
    updated_count = 0
    total_debt = 0.0
    
    for it in items:
        mid = it["marketId"].lower()
        st = it.get("state") or {}
        borrow_usd = st.get("borrowAssetsUsd") or 0.0
        
        if mid in key_to_pazar:
            key_to_pazar[mid]["borc_usd"] = round(borrow_usd, 2)
            updated_count += 1
            total_debt += borrow_usd
            
    tmp_path = pazarlar_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        
    os.replace(tmp_path, pazarlar_path)
    # Ensure current timestamp is set
    os.utime(pazarlar_path, None)
    
    print(f"Successfully updated {updated_count}/{len(market_keys)} markets.")
    print(f"Total monitored debt USD: ${total_debt:,.2f}")
    return True

if __name__ == "__main__":
    sync_markets()
