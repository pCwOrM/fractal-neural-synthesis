import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root", timeout=15)
sftp = ssh.open_sftp()

# 1. Patch /opt/apps/werracle/radar_router.py
router_path = "/opt/apps/answerr/api/radar_router.py"
with sftp.file(router_path, "r") as f:
    router_code = f.read().decode("utf-8")

changed_router = False
if "(Steakhouse, Gauntlet, Re7)" in router_code:
    router_code = router_code.replace("(Steakhouse, Gauntlet, Re7)", "(Steakhouse, Gauntlet, Moonwell)")
    changed_router = True
    print("Replaced (Steakhouse, Gauntlet, Re7) -> (Steakhouse, Gauntlet, Moonwell) in radar_router.py")

if 'rel="canonical"' not in router_code and "<title>Werracle OEV & Liquidation Sensory Radar</title>" in router_code:
    router_code = router_code.replace(
        "<title>Werracle OEV & Liquidation Sensory Radar</title>",
        '<title>Werracle OEV & Liquidation Sensory Radar</title>\n    <link rel="canonical" href="https://radar.werracle.com/v1/radar/dashboard">'
    )
    changed_router = True
    print("Added canonical link to dashboard in radar_router.py")

if "<!--email_off-->" not in router_code and "curl -X POST https://api.werracle.com/v1/radar/auth/claim-key" in router_code:
    router_code = router_code.replace(
        "curl -X POST https://api.werracle.com/v1/radar/auth/claim-key",
        "<!--email_off-->curl -X POST https://api.werracle.com/v1/radar/auth/claim-key"
    ).replace(
        '{"tx_hash": "0xYOUR_TRANSACTION_HASH", "tier": "pro", "email": "you@company.com"}\'',
        '{"tx_hash": "0xYOUR_TRANSACTION_HASH", "tier": "pro", "email": "you@company.com"}\'<!--/email_off-->'
    )
    changed_router = True
    print("Added <!--email_off--> around curl command in radar_router.py")

if changed_router:
    with sftp.file(router_path, "w") as f:
        f.write(router_code.encode("utf-8"))
    stdin, stdout, stderr = ssh.exec_command("systemctl restart answerr-api.service")
    stdout.read()
    print("Restarted answerr-api.service!")

# 2. Patch static pages in /var/www/werracle-radar/
static_pages = {
    "docs.html": "https://radar.werracle.com/docs",
    "status.html": "https://radar.werracle.com/status",
    "terms.html": "https://radar.werracle.com/terms",
    "privacy.html": "https://radar.werracle.com/privacy",
    "sla.html": "https://radar.werracle.com/sla",
}

for fname, canon_url in static_pages.items():
    fpath = f"/var/www/werracle-radar/{fname}"
    with sftp.file(fpath, "r") as f:
        html = f.read().decode("utf-8")
    modified = False
    if 'rel="canonical"' not in html and "</title>" in html:
        html = html.replace("</title>", f'</title>\n  <link rel="canonical" href="{canon_url}">', 1)
        modified = True
    if fname == "docs.html" and "<!--email_off-->" not in html:
        html = html.replace("<pre>", "<!--email_off--><pre>").replace("</pre>", "</pre><!--/email_off-->")
        modified = True
    if modified:
        with sftp.file(fpath, "w") as f:
            f.write(html.encode("utf-8"))
        print(f"Updated {fname} with canonical tag and email_off protection")

sftp.close()
ssh.close()
