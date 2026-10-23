TARGET = "/opt/apps/answerr/api/server.py"

with open(TARGET, "r", encoding="utf-8") as f:
    content = f.read()

old_cond = "    if request.url.path not in _FREE_PATHS:"
new_cond = "    if request.url.path not in _FREE_PATHS and not request.url.path.startswith('/v1/radar'):"

if old_cond in content:
    content = content.replace(old_cond, new_cond)
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated server.py to allow public access to /v1/radar")
else:
    print("WARNING: old_cond not found or already patched!")
