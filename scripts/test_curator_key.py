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
    print("HTTP Code:", resp.status)
    data = json.loads(resp.read().decode())
    print("Vault:", data.get("vault"))
    print("Shocks count:", len(data.get("shocks", [])))
    if data.get("shocks"):
        print("Sample shock -20%:", data["shocks"][4])
