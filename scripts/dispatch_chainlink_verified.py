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

RECIPIENT = "research@chainlinklabs.com"
SUBJECT = "Empirical Research & Dataset: 98.1% Value Recapture in Chainlink SVR Liquidations on Base"

BODY = """Dear Chainlink Labs Research Team,

We are sharing an independent empirical study and open replication dataset analyzing Chainlink Smart Value Recapture (SVR) and MEV liquidation dynamics on Base L2:

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dağlı (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dağlı (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Dağhan Dağlı (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure: ITouch Systems Engineering Team (Çukurova Teknokent)

Summary of Empirical Findings:
1. Base L2 (Chainlink SVR & Atlas): Across 105 multi-call verified SVR liquidation transactions ($190,506.31 gross value), competitive solver bidding redirected $186,889.85 (98.10%) directly back to lending protocols and depositors as bids.
2. Solver Margins: Solvers retained a pre-swap gross margin of only 1.86% ($3,545.73), with median transaction margins compressed to -1.55%. Over 61.9% (65 of 105) of transactions concluded at zero or negative net profit prior to off-chain DEX slippage.
3. Ethereum L1 Contrast: Across 1,049 analyzed L1 liquidation events, builder payments were heavily concentrated: the top 22 transactions accounted for $344,155.62 of the total $358,316.62 paid to builders (96.0%), while 80.84% were micro-payments under $1.00.

Dataset & Reproducibility Links:
- Hugging Face Hub (Live v1.2): https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026
- Permanent Zenodo DOI (Record 23642090): https://doi.org/10.5281/zenodo.23623588
- SSRN Preprint: https://papers.ssrn.com/abstract=7668638
- Live Risk & Liquidation Radar: https://radar.werracle.com

We welcome feedback from the Chainlink Labs Research team and are glad to provide dedicated API feeds or collaborate on further sub-block MEV telemetry.

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

print("SUCCESS: Outreach email dispatched to research@chainlinklabs.com (BCC: pcworm@pcworm.net)!")
