import subprocess

SRC = "/opt/apps/werracle/health/werracle_morpho_golge.py"

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# Revert STABLE back to pure stablecoins
bad_stable = 'STABLE = ("USDC", "USDT", "DAI", "USDS", "EURC", "USDBC", "GHO", "USDE", "WETH", "CBBTC", "CBETH")'
good_stable = 'STABLE = ("USDC", "USDT", "DAI", "USDS", "EURC", "USDBC", "GHO", "USDE")'

if bad_stable in content:
    content = content.replace(bad_stable, good_stable, 1)
    print("Reverted STABLE back to stablecoins only (removed WETH/CBBTC/CBETH).")
else:
    print("Warning: bad_stable string not found.")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

# Syntax check
res = subprocess.run(["/opt/apps/answerr/venv/bin/python3", "-m", "py_compile", SRC], capture_output=True, text=True)
if res.returncode == 0:
    print("Python syntax compile OK!")
else:
    print(f"Compilation error: {res.stderr}")
    sys.exit(1)
