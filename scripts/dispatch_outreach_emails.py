import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

dispatch_code = '''import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from datetime import datetime, timezone

with open("/opt/apps/werracle/reporting/mail_creds.json") as f:
    creds = json.load(f)

BCC_ADDR = "pcworm@pcworm.net"
FROM_ADDR = "ask@answerr.me"
FROM_DISPLAY = "Volkan Dagli | Werracle & ITouch Systems <ask@answerr.me>"

emails = [
    {
        "id": "chainlink",
        "to": "research@chain.link",
        "subject": "Empirical SVR Value Recapture & Multi-Call Liquidation Data on Base (Dataset v1.2 & Replication Decoder)",
        "body": """Dear Chainlink Research & SVR Engineering Team,

We have completed an empirical analysis of Smart Value Recapture (SVR) liquidation transactions on Base across the October 2026 volatility window, and wanted to share our replication dataset and findings directly with your team.

Key empirical findings from our audited sample (Base, 2–22 October 2026, 105 multi-call liquidation transactions, with 87 occurring in the 12–18 October window):

1. Value Recapture Efficiency: Across the sample, SVR contracts successfully recaptured $179,833.68 of the $190,506.31 gross liquidation incentive (94.38% aggregate incentive-weighted recapture). The median per-transaction recapture rate reached 98.30%.
2. Solver Margin Compression: Median solver margin was compressed to -1.55% (solvers subsidized gas via priority fees and competitive bidding), confirming strong auction competition.
3. Contrast with Ethereum L1: On Ethereum L1 non-SVR Morpho liquidations (1,049 analyzed transactions), builder payments exhibit extreme fat-tail concentration: the 22 largest liquidation transactions account for 95.94% ($351,268 of $366,113) of all builder bribe payments.

The complete dataset, raw execution traces, and reproduction scripts have been deposited under open-access licenses:
- Zenodo Record (DOI: 10.5281/zenodo.22942598): Full transaction manifest and CSV/JSONL traces.
- Hugging Face Repository: https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026 (CC-BY-4.0).
- Replication Engine: All 54 summary metrics can be independently verified by running `reproduce_summary.py` against raw RPC traces.
- Live Telemetry Observatory: https://radar.werracle.com (actively monitoring 38 verified lending markets and $2.20B+ in clean borrow debt).

Our research paper is available on arXiv (2609.30719 [cs.CR, cs.AI]) and Elsevier SSRN (7626279). We welcome your feedback, methodology critiques, or potential collaboration on empirical OEV mitigation metrics.

Sincerely,

Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University)
Dr. Zerrin Dagli (Academic Advisor, Mersin University)
Daghan Dagli (Student Researcher, Toros University / Toros Science High School)
and the ITouch Systems Core Engineering Team

ITouch Systems (Çukurova Teknokent, Adana / Turkey)
ORCID: 0009-0000-1587-8703
Direct Email: ask@answerr.me / pcworm@pcworm.net
Observatory: https://radar.werracle.com
Corporate: https://werracle.com
"""
    },
    {
        "id": "steakhouse",
        "to": "info@steakhouse.financial",
        "subject": "Independent Collateral Shock Stress-Test Telemetry for Steakhouse USDC Vault (Base)",
        "body": """Hi Steakhouse Team,

We have developed an independent, real-time liquidation telemetry and collateral shock simulation engine for Morpho Blue vaults, currently live at https://radar.werracle.com.

We ran an on-chain stress-simulation specifically against the Steakhouse USDC vault on Base (0xbeeF010f9cb27031ad51e3333f9aF9C6B1228183, ~$115.7M TVL, 5 collateral markets). At the time of writing (based on live on-chain Morpho state), our granular borrower model indicates:

- Baseline (Current Prices): 0 liquidatable positions, $0.00 bad debt across your allocated markets.
- -15% Collateral Price Shock: 2,643 market positions become liquidatable ($133.5M debt). Across the entire market, bad debt is estimated at $225.7k, resulting in an estimated pro-rata bad debt exposure for Steakhouse USDC of $12,261.59 (0.01% of TVL).
- -20% Collateral Price Shock: 3,674 positions reach liquidation ($215.3M debt). Estimated total market bad debt is $2.69M, with Steakhouse USDC's pro-rata exposure modeled at $150,097.63 (~0.13% of TVL).
- -30% Severe Shock: 6,365 positions affected ($526.2M debt). Modeled vault exposure reaches $1.28M (~1.10% of TVL).

Methodology Notes:
- Losses are calculated pro-rata based on your vault's current supply share across individual Morpho market allocations (reflecting Morpho's proportional loss distribution, without synthetic senior tiering assumptions).
- Potential SVR value recapture is tracked separately (proceeds accrue to protocol/SVR contracts, not to vault balance sheets).
- 45 unlisted/synthetic spam markets have been filtered out to ensure pure institutional data.

If you would like to inspect the raw borrower health distributions or test this endpoint directly in your risk models, reply to this email with your preferred wallet address or corporate email, and we will provision a dedicated 30-day Institutional evaluation key (3,000 req/min) for your risk desk.

Live curator endpoint specification: https://api.werracle.com/docs
Observatory: https://radar.werracle.com

Best regards,

Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University)
Dr. Zerrin Dagli (Academic Advisor, Mersin University)
Daghan Dagli (Student Researcher, Toros University / Toros Science High School)
and the ITouch Systems Core Engineering Team

ITouch Systems (Çukurova Teknokent, Adana / Turkey)
Direct Email: ask@answerr.me / pcworm@pcworm.net
https://werracle.com | https://radar.werracle.com
"""
    },
    {
        "id": "gauntlet",
        "to": "gov@gauntlet.xyz",
        "subject": "Sub-Block Liquidation Telemetry & Collateral Shock Simulation for Morpho Curators",
        "body": """Hi Gauntlet Team,

We have deployed an automated real-time risk telemetry observatory for Morpho Blue markets, actively tracking $2.20B+ in verified borrow debt across 38 listed markets on Base and Ethereum L1: https://radar.werracle.com.

Our engine performs continuous borrower health-factor stratification and simulates instant collateral price shocks (-5% to -30%) mapped to active vault supply allocations. Key capabilities designed for quantitative risk curators include:

1. Pro-Rata Bad Debt Simulation: Granular, position-by-position calculation of liquidation premiums and uncovered debt under extreme slippage scenarios.
2. Verified SVR Telemetry: Tracking empirical solver bids and value recapture efficiency across multi-call bundles (94.38% aggregate recapture measured on Base across 105 liquidations).
3. Synthetic Market Hygiene: Automated filtering of 45 unlisted/zero-liquidity collateral pairs ($2.31B in synthetic debt noise isolated from core risk matrices).

If your engineering or risk team would like to test our REST API or high-frequency websocket risk stream against your staging models, reply to this email and we will instantly provision a 30-day Institutional evaluation key.

Interactive API Docs: https://api.werracle.com/docs
Empirical Research Paper: arXiv:2609.30719 [cs.CR] / SSRN: 7626279
Observatory: https://radar.werracle.com

Best regards,

Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University)
Dr. Zerrin Dagli (Academic Advisor, Mersin University)
Daghan Dagli (Student Researcher, Toros University / Toros Science High School)
and the ITouch Systems Core Engineering Team

ITouch Systems (Çukurova Teknokent, Adana / Turkey)
Direct Email: ask@answerr.me / pcworm@pcworm.net
https://werracle.com | https://radar.werracle.com
"""
    }
]

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(creds["smtp_host"], creds["smtp_port"], context=ctx, timeout=30) as s:
    s.login(creds["smtp_user"], creds["smtp_pass"])
    for em in emails:
        msg = MIMEText(em["body"], "plain", "utf-8")
        msg["Subject"] = em["subject"]
        msg["From"] = FROM_DISPLAY
        msg["To"] = em["to"]
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="answerr.me")
        msg["Reply-To"] = "ask@answerr.me"
        
        recipients = [em["to"], BCC_ADDR]
        s.sendmail(FROM_ADDR, recipients, msg.as_string())
        print(f"SENT: {em['id']} -> {em['to']} (BCC: {BCC_ADDR})")

print("ALL_DISPATCH_COMPLETE_SUCCESS")
'''

sftp = ssh.open_sftp()
with sftp.file("/tmp/dispatch_outreach.py", "w") as f:
    f.write(dispatch_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("/usr/bin/python3 /tmp/dispatch_outreach.py && rm -f /tmp/dispatch_outreach.py")
output = stdout.read().decode('utf-8', errors='ignore')
errors = stderr.read().decode('utf-8', errors='ignore')

print("Dispatch Output:\n", output)
print("Dispatch Errors:\n", errors)

ssh.close()
