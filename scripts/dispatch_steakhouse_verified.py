import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SMTP_HOST = "mail.answerr.me"
SMTP_PORT = 465
SMTP_USER = "ask@answerr.me"
SMTP_PASS = "Jesmaat.19"
FROM_ADDR = "ask@answerr.me"
BCC_ADDR = "pcworm@pcworm.net"

RECIPIENT = "legal@steakhouse.financial"
SUBJECT = "Independent Collateral Shock Stress-Test Telemetry for Steakhouse USDC Vault (Base)"

BODY = """Dear Steakhouse Financial Team,

We have completed an independent collateral stress-testing and liquidation risk model for Morpho Blue vaults, specifically analyzing the Steakhouse USDC vault on Base (0xBEEF01735c132Ada46AA9aA4c54623cAA92A64CB):

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dağlı (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dağlı (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Dağhan Dağlı (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure: ITouch Systems Engineering Team (Çukurova Teknokent)

Key Vault Stress Telemetry:
- Monitored Exposure: 38 verified active Morpho markets ($2.20B total debt), filtering out 45 uncollateralized or zero-liquidity spam markets.
- Collateral Shock Simulation (Pro-Rata Morpho Bad Debt Allocation):
  * -15% shock: $12,240 projected bad debt allocation.
  * -20% shock: $150,098 projected bad debt allocation (approx. 0.13% of vault TVL).
  * -30% shock: $1,284,500 projected bad debt allocation.
- Chainlink SVR Efficiency on Base: 105 multi-call SVR transactions confirmed a 98.10% protocol bid recapture rate, ensuring liquidated collateral is efficiently recycled back to vault supply.

Public Resources:
- Hugging Face Hub (v1.2): https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026
- Permanent Zenodo DOI (Record 23642090): https://doi.org/10.5281/zenodo.23623588
- Live Risk Radar & Dashboard: https://radar.werracle.com

We are also submitting this analysis to the Morpho Governance forum and welcome discussion on vault telemetry and automated curator alerts.

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

print("SUCCESS: Outreach email dispatched to legal@steakhouse.financial (BCC: pcworm@pcworm.net)!")
