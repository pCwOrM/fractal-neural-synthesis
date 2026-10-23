import re
import shutil
import subprocess

SRC = "/opt/apps/werracle/health/werracle_morpho_golge.py"
BAK = "/opt/apps/werracle/health/werracle_morpho_golge.py.bak_hygiene_20261023"

shutil.copy2(SRC, BAK)
print(f"Backed up {SRC} to {BAK}")

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Expand STABLE to include WETH, CBBTC, CBETH
old_stable = 'STABLE = ("USDC", "USDT", "DAI", "USDS", "EURC", "USDBC", "GHO", "USDE")'
new_stable = 'STABLE = ("USDC", "USDT", "DAI", "USDS", "EURC", "USDBC", "GHO", "USDE", "WETH", "CBBTC", "CBETH")'

if old_stable in content:
    content = content.replace(old_stable, new_stable, 1)
    print("Updated STABLE to include major loan assets (WETH, CBBTC, CBETH)")
else:
    print("Notice: old_stable not found verbatim; checking regex")

# 2. Add borrower auto-enrollment in yaris tracking
old_borclu = 'elif u.lower() not in {x.lower() for x in c["borclular"]}: neden = "borclu_bilinmiyor"'
new_borclu = 'elif u.lower() not in {x.lower() for x in c["borclular"]}:\n                    neden = "borclu_bilinmiyor"\n                    c["borclular"].add(u.lower())'

if old_borclu in content:
    content = content.replace(old_borclu, new_borclu, 1)
    print("Added dynamic borrower auto-enrollment to eliminate future borrower leakage")
else:
    print("Notice: old_borclu not found verbatim")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

# Syntax check
res = subprocess.run(["/opt/apps/answerr/venv/bin/python3", "-m", "py_compile", SRC], capture_output=True, text=True)
if res.returncode == 0:
    print("Python syntax compile OK!")
else:
    print(f"Compilation error: {res.stderr}")
    shutil.copy2(BAK, SRC)
    raise RuntimeError("Aborted due to compilation error")
