import os
import urllib.request, json

url = "https://api.werracle.com/v1/radar/curator/steakhouse"
req = urllib.request.Request(
    url,
    headers={
        "X-API-Key": os.environ.get("WERRACLE_RADAR_KEY", "wrk_inst_live_sample"),
        "User-Agent": "SteakhouseTest/1.0"
    }
)

with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())
    print("worst_case_vault_bad_debt_pct_of_tvl:", data.get("worst_case_vault_bad_debt_pct_of_tvl"))
    print("stress_test keys:", list(data.get("stress_test", {}).keys()))
    for k, v in data.get("stress_test", {}).items():
        print(f"Shock {k}: liquidatable_debt=${v.get('liquidatable_debt_usd', 0):,.2f}, bad_debt=${v.get('market_bad_debt_usd', 0):,.2f}, vault_share=${v.get('vault_bad_debt_usd', 0):,.2f}")
