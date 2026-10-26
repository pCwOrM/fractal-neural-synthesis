import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, formataddr
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SMTP_HOST = "mail.answerr.me"
SMTP_PORT = 465
SMTP_USER = "ask@answerr.me"
SMTP_PASS = "Jesmaat.19"
FROM_ADDR = "ask@answerr.me"
FROM_NAME = "Volkan Dagli - Werracle & ITouch Systems"
BCC_ADDR = "pcworm@pcworm.net"

OUTREACH_TARGETS = [
    {
        "name": "Chainlink Labs Research",
        "to": "research@chainlinklabs.com",
        "subject": "Empirical Research & Dataset: 98.1% Value Recapture in Chainlink SVR Liquidations on Base",
        "body": """Dear Chainlink Labs Research Team,

We are sharing an independent empirical study and open replication dataset analyzing Chainlink Smart Value Recapture (SVR) and MEV liquidation dynamics on Base L2:

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dagli (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Daghan Dagli (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure & Attribution: ITouch Systems Engineering Team (Cukurova Teknokent)

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

Volkan Dagli
Co-Founder & CTO, ITouch Systems
Anadolu University
ask@answerr.me | https://werracle.io
"""
    },
    {
        "name": "Gauntlet",
        "to": "support@gauntlet.xyz",
        "subject": "Empirical Liquidation Telemetry & Pro-Rata Bad Debt Modeling (Werracle Radar)",
        "body": """Dear Gauntlet Team,

We are sharing empirical research and live risk telemetry from Werracle Radar covering lending liquidations and bad debt dynamics across Base and Ethereum L1:

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dagli (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Daghan Dagli (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure & Attribution: ITouch Systems Engineering Team (Cukurova Teknokent)

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

Volkan Dagli
Co-Founder & CTO, ITouch Systems
Anadolu University
ask@answerr.me | https://werracle.io
"""
    },
    {
        "name": "Steakhouse Financial",
        "to": "legal@steakhouse.financial",
        "subject": "Independent Collateral Shock Stress-Test Telemetry for Steakhouse USDC Vault (Base)",
        "body": """Dear Steakhouse Financial Team,

We have completed an independent collateral stress-testing and liquidation risk model for Morpho Blue vaults, specifically analyzing the Steakhouse USDC vault on Base (0xBEEF01735c132Ada46AA9aA4c54623cAA92A64CB):

Title: Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1
Authors:
- Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University; ORCID: 0009-0000-1587-8703)
- Dr. Zerrin Dagli (Academic Advisor, Mersin University; ORCID: 0000-0001-9490-6425)
- Daghan Dagli (Student Researcher, Toros University / Toros Science High School; ORCID: 0009-0003-2492-8313)
Infrastructure & Attribution: ITouch Systems Engineering Team (Cukurova Teknokent)

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

We are also sharing this analysis on the Morpho Governance forum and welcome discussion on vault telemetry and automated curator alerts.

Best regards,

Volkan Dagli
Co-Founder & CTO, ITouch Systems
Anadolu University
ask@answerr.me | https://werracle.io
"""
    }
]

def main():
    print("=== CONNECTING TO SMTP SERVER ===")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.login(SMTP_USER, SMTP_PASS)
        for target in OUTREACH_TARGETS:
            msg = MIMEMultipart()
            # STRICT RFC 5322 ASCII formataddr
            msg['From'] = formataddr((FROM_NAME, FROM_ADDR))
            msg['To'] = target['to']
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = target['subject']
            msg['Reply-To'] = FROM_ADDR
            msg.attach(MIMEText(target['body'], 'plain', 'utf-8'))

            recipients = [target['to'], BCC_ADDR]
            print(f"Dispatching to {target['name']} ({target['to']}) with BCC to {BCC_ADDR}...")
            server.sendmail(FROM_ADDR, recipients, msg.as_string())
            print(f"  -> Dispatched successfully to {target['to']}!")
            time.sleep(2)

    print("\nAll outreach emails dispatched cleanly under RFC 5322 compliance.")

if __name__ == "__main__":
    main()
