import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SMTP_HOST = "mail.answerr.me"
SMTP_PORT = 465
SMTP_USER = "ask@answerr.me"
SMTP_PASS = os.environ.get("ANSWERR_MAIL_PASS", "")
FROM_ADDR = "ask@answerr.me"
BCC_ADDR = "pcworm@pcworm.net"

RECIPIENT = "support@gauntlet.xyz"
SUBJECT = "Empirical Liquidation Telemetry & Pro-Rata Bad Debt Modeling (Werracle Radar)"

BODY = """Dear Gauntlet Team,

We are sharing empirical research and live risk telemetry from Werracle Radar covering lending liquidations and bad debt dynamics across Base and Ethereum L1:

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dağlı (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dağlı (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Dağhan Dağlı (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure: ITouch Systems Engineering Team (Çukurova Teknokent)

Key Research Highlights:
1. Base L2 SVR Bidding: 105 multi-call SVR liquidations totaling $190,506.31 gross value demonstrated a 98.10% protocol bid recapture rate ($186,889.85), compressing solver margins to a median of -1.55%.
2. Morpho Vault Risk Telemetry: Our risk model continuously monitors 38 active verified Morpho markets ($2.20B total debt), filtering out 45 uncollateralized or zero-liquidity spam markets. It simulates collateral shock scenarios with exact pro-rata debt allocation.
3. Open Science & Data Replication: The complete reproduction package, code, and raw transaction data are published under Open Science standards.

Links:
- Hugging Face Hub (v1.2): https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026
- Permanent Zenodo DOI (Record 23642090): https://doi.org/10.5281/zenodo.23623588
- SSRN Preprint: https://papers.ssrn.com/abstract=7668638
- Live Risk & Liquidation Radar: https://radar.werracle.com

We would be pleased to provide custom sub-block liquidation telemetry feeds or collaborate on joint risk modeling for lending protocols.

Best regards,

Volkan Dağlı
Co-Founder & CTO, ITouch Systems
Anadolu University
ask@answerr.me | https://werracle.io
"""

msg = MIMEMultipart()
msg['From'] = f"Volkan Dağlı | Werracle & ITouch Systems <{FROM_ADDR}>"
msg['To'] = RECIPIENT
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = SUBJECT
msg['Reply-To'] = FROM_ADDR
msg.attach(MIMEText(BODY, 'plain', 'utf-8'))

all_recipients = [RECIPIENT, BCC_ADDR]

print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} via SSL...")
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15) as server:
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(FROM_ADDR, all_recipients, msg.as_string())

print("SUCCESS: Outreach email dispatched to support@gauntlet.xyz (BCC: pcworm@pcworm.net)!")
