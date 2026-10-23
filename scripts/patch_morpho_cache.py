import os
import shutil

TARGET = "/opt/apps/werracle/health/werracle_morpho_golge.py"
BACKUP = "/opt/apps/werracle/health/werracle_morpho_golge.py.bak_pre_adim3_20261023"

# 1. Backup
if not os.path.exists(BACKUP):
    shutil.copy2(TARGET, BACKUP)
    print(f"Created backup at {BACKUP}")
else:
    print(f"Backup already exists at {BACKUP}")

with open(TARGET, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Patch discover()
old_discover_part = """def discover(archive_url=None):
    if os.path.exists(CACHE):
        try:
            cached = json.load(open(CACHE))
            cache_age = time.time() - os.path.getmtime(CACHE)
            if cache_age < 7 * 86400:
                return cached
            # 7 gun asildi: RPC 429 çökmesini engellemek için artimli guncelleme dene, hata durumunda mevcut onbellekle DEVAM ET
            log.info(f"Pazar onbellegi {cache_age/86400:.1f} gunluk; artimli guncelleme deneniyor...")
            try:
                w = Web3(Web3.HTTPProvider(archive_url, request_kwargs={"timeout": 20})) if archive_url else W3[0]
                head = w.eth.block_number
                cached_block = cached.get("blok", DEPLOY_BLOCK)
                if head > cached_block:
                    allids = ["0x" + c["id"] for c in cached.get("pazarlar", [])]
                    new_users = collections.defaultdict(set)
                    for l in logs_range(w, {"address": MORPHO, "topics": [T_BORROW, allids]}, cached_block + 1, head):
                        new_users[l["topics"][1].hex().replace("0x", "")].add("0x" + l["topics"][2].hex()[-40:])
                    for c in cached.get("pazarlar", []):
                        c["borclular"] = sorted(set(c.get("borclular", [])) | new_users[c["id"]])
                    cached["blok"] = head
                    json.dump(cached, open(CACHE + ".tmp", "w"))
                    os.replace(CACHE + ".tmp", CACHE)
                    log.info(f"Pazar onbellegi artimli guncellendi (blok {head}).")
                else:
                    os.utime(CACHE, None)
                return cached
            except Exception as update_err:
                log.warning(f"Onbellek artimli guncellemesi basarisiz (RPC 429/timeout): {update_err}. Mevcut {len(cached.get('pazarlar',[]))} pazarla guvenli devam ediliyor.")
                os.utime(CACHE, None) # 7 gunluk saati sifirla, her yeniden baslatmada tekrar RPC zorlamasin
                return cached
        except Exception as read_err:
            log.error(f"Onbellek okuma hatasi: {read_err}")"""

new_discover_part = """def discover(archive_url=None):
    if os.path.exists(CACHE):
        try:
            cached = json.load(open(CACHE))
            cache_age = time.time() - os.path.getmtime(CACHE)
            if cache_age < 7 * 86400:
                return cached
            # 7 gun asildi: 28 Ekim oncesi onbellek koruma yamasi (Adim 3)
            log.info(f"Pazar onbellegi {cache_age/86400:.1f} gunluk; guvenli yenileme kontrol ediliyor...")
            if not archive_url:
                # Halka acik RPC'lerde toplu eth_getLogs aninda 429 verir; 14 sn timeout beklemeden mevcut pazarlarla devam et
                log.info(f"Ozel arsiv RPC tanimli degil. Mevcut {len(cached.get('pazarlar',[]))} pazar ve canli borclular.json ile kesintisiz devam ediliyor.")
                os.utime(CACHE, None)
                return cached
            try:
                w = Web3(Web3.HTTPProvider(archive_url, request_kwargs={"timeout": 20}))
                head = w.eth.block_number
                cached_block = cached.get("blok", DEPLOY_BLOCK)
                if head > cached_block:
                    allids = ["0x" + c["id"] for c in cached.get("pazarlar", [])]
                    new_users = collections.defaultdict(set)
                    for l in logs_range(w, {"address": MORPHO, "topics": [T_BORROW, allids]}, cached_block + 1, head):
                        new_users[l["topics"][1].hex().replace("0x", "")].add("0x" + l["topics"][2].hex()[-40:])
                    for c in cached.get("pazarlar", []):
                        c["borclular"] = sorted(set(c.get("borclular", [])) | new_users[c["id"]])
                    cached["blok"] = head
                    json.dump(cached, open(CACHE + ".tmp", "w"))
                    os.replace(CACHE + ".tmp", CACHE)
                    log.info(f"Pazar onbellegi artimli guncellendi (blok {head}).")
                else:
                    os.utime(CACHE, None)
                return cached
            except Exception as update_err:
                log.warning(f"Onbellek artimli guncellemesi basarisiz (RPC 429/timeout): {update_err}. Mevcut {len(cached.get('pazarlar',[]))} pazarla guvenli devam ediliyor.")
                os.utime(CACHE, None)
                return cached
        except Exception as read_err:
            log.error(f"Onbellek okuma hatasi: {read_err}")"""

if old_discover_part in content:
    content = content.replace(old_discover_part, new_discover_part)
    print("Successfully patched discover()")
else:
    print("ERROR: old_discover_part not found in content!")

# 3. Patch _race_loop_ic() sleep & backoff
old_race_part = """def _race_loop_ic():
    last = None
    while True:
        time.sleep(4)"""

new_race_part = """def _race_loop_ic():
    last = None
    while True:
        time.sleep(8)"""

if old_race_part in content:
    content = content.replace(old_race_part, new_race_part)
    print("Successfully patched _race_loop_ic() polling interval (4s -> 8s)")
else:
    print("WARNING: old_race_part exact match not found; checking alternatives...")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {TARGET}")
