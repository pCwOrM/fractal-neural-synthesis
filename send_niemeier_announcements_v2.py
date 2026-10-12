#!/usr/bin/env python3
"""
send_niemeier_announcements_v2.py
=============================================================================
WERR Ecosystem Sovereign Dispatcher v2:
- Fixed Sender to strict 'ask@answerr.me' (RFC 5322 compliant, avoids Gmail/Lean FRO bounce).
- Primary email for Volkan Dağlı: pcworm@pcworm.net (NO gmail!).
- Target for Prof. John Duncan: jduncan@gate.sinica.edu.tw (Academia Sinica, Emory bounced).
- Target for Prof. Miranda Cheng: mcheng@uva.nl (UvA delivered cleanly!).
- Target for Lean FRO: contact@lean-fro.org with clean RFC headers.
=============================================================================
"""

import sys
import os
import json
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CONFIG_PATH = os.path.expanduser("~/.answerr/mail.json")

def load_credentials():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return "mail.answerr.me", 465, cfg["email"], cfg["password"]

SMTP_SERVER, SMTP_PORT, AUTH_USER, AUTH_PASS = load_credentials()

EMAILS = [
    {
        "recipient": "jduncan@gate.sinica.edu.tw",
        "name": "Prof. John F. R. Duncan (Academia Sinica / Emory)",
        "subject": "Machine-Certified Formalization of Niemeier Lattice A_8^3 & Umbral Moonshine in Lean 4",
        "body": """Dear Professor Duncan,

I hope this email finds you well.

Our research group at ITouch Systems has formally specified and machine-certified the 24-dimensional Niemeier lattice A_8^3, its ternary glue code, K3 du Val singularity resolutions, and Umbral Moonshine lambency (l = 9) in Lean 4 with 0 sorry.

Key Highlights of the Formalization:
1. Exact metric verification of the ternary glue code: isotropic generator norm ||g||^2 = 4 (even integer) ensuring unimodularity det(N) = 1.0000.
2. Exact topological matching of the K3 Euler characteristic chi(X) = 24 with lattice rank 24.
3. Machine certification of the lambency l = 9 vector-valued mock modular form structure (weight 1/2) and shadow unary theta series (weight 3/2).

The project is permanently minted on CERN Zenodo and published openly on GitHub:
- CERN Zenodo: https://zenodo.org/records/23324067 (DOI: 10.5281/zenodo.23324066)
- GitHub Repository: https://github.com/pCwOrM/niemeier-a8-umbral-moonshine
- Monograph PDF: https://github.com/pCwOrM/niemeier-a8-umbral-moonshine/blob/main/Niemeier_A8_K3_Umbral_Moonshine_Formalization.pdf

We hope this machine-certified bridge into Lean 4 serves as a valuable resource for the Moonshine community.

With highest regards,

Volkan Dağlı
ITouch Systems Research Group & Anadolu University
ask@answerr.me │ pcworm@pcworm.net
ORCID: 0009-0000-1587-8703
"""
    },
    {
        "recipient": "contact@lean-fro.org",
        "name": "Lean FRO Team",
        "subject": "New Formalization Release: 24D Niemeier Lattice A_8^3 & K3 Umbral Moonshine in Lean 4",
        "body": """Dear Lean FRO Team,

We are pleased to announce the open-source release and permanent CERN Zenodo minting of a standalone Lean 4 formalization:

"Machine-Certified Formalization of the 24-Dimensional Niemeier Lattice A_8^3, K3 Hodge Duality and Umbral Moonshine"
Authors: Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı; Contributor: Bekirhan Dağlı

Highlights:
- Formalizes the 24D even unimodular Niemeier lattice A_8^3 (Coxeter number h = 9, 216 roots).
- Proves ternary glue code isotropic norm ||g||^2 = 4 and unimodularity det = 1 with 0 sorry.
- Connects topological K3 invariants (chi = 24) and Umbral Moonshine lambency l = 9.
- Verified in Lean v4.21.0 with an accompanying exact Python algebraic test oracle.

Links:
- Zenodo Record: https://zenodo.org/records/23324067 (DOI: 10.5281/zenodo.23324066)
- GitHub: https://github.com/pCwOrM/niemeier-a8-umbral-moonshine

We would love for this package to be indexed in the broader Lean 4 mathematical ecosystem and community catalogs.

Best regards,

Volkan Dağlı
ITouch Systems & Anadolu University
ask@answerr.me │ pcworm@pcworm.net
"""
    }
]

def dispatch_clean(target):
    msg = MIMEMultipart()
    msg["From"] = "ask@answerr.me"
    msg["To"] = target["recipient"]
    msg["Subject"] = target["subject"]
    msg["Reply-To"] = "ask@answerr.me, pcworm@pcworm.net"
    msg.attach(MIMEText(target["body"], "plain", "utf-8"))

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=20) as server:
        server.login(AUTH_USER, AUTH_PASS)
        server.sendmail(AUTH_USER, [target["recipient"]], msg.as_string())
    print(f"[+] Successfully delivered to {target['name']} <{target['recipient']}> via {SMTP_SERVER}:465")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry-run"
    if mode == "send":
        print(f"[*] Dispatching corrected announcements via {SMTP_SERVER}:{SMTP_PORT}...")
        for target in EMAILS:
            try:
                dispatch_clean(target)
            except Exception as e:
                print(f"[-] Error sending to {target['recipient']}: {e}")
        print("[+] All dispatches processed.")
    else:
        print("[*] Dry-run mode for corrected dispatch:")
        for target in EMAILS:
            print(f"  - Ready for: {target['name']} <{target['recipient']}>")
