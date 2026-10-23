import urllib.request
import json

base_url = "http://127.0.0.1:8560"

endpoints = [
    "/v1/health",
    "/v1/radar/overview",
    "/v1/radar/chains",
    "/v1/radar/oev-analytics",
    "/v1/radar/solvers?limit=3",
    "/v1/radar/hot-positions?limit=3",
    "/v1/radar/dashboard"
]

print("--- Testing Live Endpoints on port 8560 ---")
for ep in endpoints:
    url = base_url + ep
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TestClient/1.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            code = res.getcode()
            body = res.read()
            size = len(body)
            preview = body[:80].decode('utf-8', errors='replace').replace('\n', ' ')
            print(f"[{code}] {ep:<30} ({size} bytes): {preview}")
    except Exception as e:
        print(f"[FAIL] {ep}: {e}")
