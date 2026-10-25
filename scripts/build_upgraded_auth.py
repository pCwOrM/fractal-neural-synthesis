import sys

with open("scripts/radar_auth_remote.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace init_db
old_init_db = """        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_tier ON api_keys(tier);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);")
    conn.close()"""

new_init_db = """        conn.execute(""" + '"""' + """
            CREATE TABLE IF NOT EXISTS rate_limits (
                key_hash TEXT NOT NULL,
                minute_bucket INTEGER NOT NULL,
                request_count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (key_hash, minute_bucket)
            );
        """ + '"""' + """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_tier ON api_keys(tier);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_rate_limits_bucket ON rate_limits(minute_bucket);")
    conn.close()"""

assert old_init_db in content, "old_init_db target not found!"
content = content.replace(old_init_db, new_init_db)

# Replace check_rate_limit
old_check_rate = """def check_rate_limit(key_hash: str, limit_per_min: int) -> bool:
    now_min = int(time.time() // 60)
    counters = _RATE_LIMIT_COUNTERS.setdefault(key_hash, {})
    
    # Clean old buckets
    old_buckets = [b for b in counters if b < now_min - 2]
    for b in old_buckets:
        del counters[b]
        
    current_count = counters.get(now_min, 0)
    if current_count >= limit_per_min:
        return False
        
    counters[now_min] = current_count + 1
    return True"""

new_check_rate = """def check_rate_limit(key_hash: str, limit_per_min: int, db_path: str = DB_PATH) -> bool:
    now_min = int(time.time() // 60)
    try:
        conn = get_db_connection(db_path)
        with conn:
            cursor = conn.execute(\"\"\"
                INSERT INTO rate_limits (key_hash, minute_bucket, request_count)
                VALUES (?, ?, 1)
                ON CONFLICT(key_hash, minute_bucket) DO UPDATE SET request_count = request_count + 1
                RETURNING request_count;
            \"\"\", (key_hash, now_min))
            row = cursor.fetchone()
            current_count = row[0] if row else 1
            if now_min % 5 == 0:
                conn.execute("DELETE FROM rate_limits WHERE minute_bucket < ?", (now_min - 5,))
        conn.close()
        return current_count <= limit_per_min
    except Exception:
        counters = _RATE_LIMIT_COUNTERS.setdefault(key_hash, {})
        old_buckets = [b for b in counters if b < now_min - 2]
        for b in old_buckets:
            del counters[b]
        current_count = counters.get(now_min, 0)
        if current_count >= limit_per_min:
            return False
        counters[now_min] = current_count + 1
        return True"""

assert old_check_rate in content, "old_check_rate target not found!"
content = content.replace(old_check_rate, new_check_rate)

with open("scripts/radar_auth_upgraded.py", "w", encoding="utf-8") as f:
    f.write(content)

print("scripts/radar_auth_upgraded.py written successfully.")
