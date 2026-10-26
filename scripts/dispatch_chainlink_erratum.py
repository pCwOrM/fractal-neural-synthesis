import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

erratum_script = '''import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

with open("/opt/apps/werracle/reporting/mail_creds.json") as f:
    creds = json.load(f)

TO_ADDR = "research@chain.link"
BCC_ADDR = "pcworm@pcworm.net"
FROM_ADDR = "ask@answerr.me"
FROM_DISPLAY = "Volkan Dagli | Werracle & ITouch Systems <ask@answerr.me>"
SUBJECT = "Re: Empirical SVR Value Recapture & Multi-Call Liquidation Data on Base (Dataset v1.2 & Replication Decoder)"

BODY = """Dear Chainlink Research Team,

Quick erratum regarding our previous email: please note that the verified Hugging Face dataset repository URL is:
https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026

(Apologies for the repository slug typo in the initial note; the Zenodo DOI 10.5281/zenodo.22942598, preprint arXiv:2609.30719, and SSRN 7626279 links remain unchanged).

Sincerely,

Volkan Dagli (Co-Founder & CTO, ITouch Systems & Anadolu University)
Dr. Zerrin Dagli (Academic Advisor, Mersin University)
Daghan Dagli (Student Researcher, Toros University / Toros Science High School)
and the ITouch Systems Core Engineering Team

ITouch Systems (Çukurova Teknokent, Adana / Turkey)
Direct Email: ask@answerr.me / pcworm@pcworm.net
Observatory: https://radar.werracle.com
Corporate: https://werracle.com
"""

msg = MIMEText(BODY, "plain", "utf-8")
msg["Subject"] = SUBJECT
msg["From"] = FROM_DISPLAY
msg["To"] = TO_ADDR
msg["Date"] = formatdate(localtime=True)
msg["Message-ID"] = make_msgid(domain="answerr.me")
msg["Reply-To"] = "ask@answerr.me"

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(creds["smtp_host"], creds["smtp_port"], context=ctx, timeout=30) as s:
    s.login(creds["smtp_user"], creds["smtp_pass"])
    recipients = [TO_ADDR, BCC_ADDR]
    s.sendmail(FROM_ADDR, recipients, msg.as_string())
    print("CHAINLINK_ERRATUM_DISPATCHED_SUCCESS")
'''

sftp = ssh.open_sftp()
with sftp.file("/tmp/dispatch_erratum.py", "w") as f:
    f.write(erratum_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("/usr/bin/python3 /tmp/dispatch_erratum.py && rm -f /tmp/dispatch_erratum.py")
output = stdout.read().decode('utf-8', errors='ignore')
errors = stderr.read().decode('utf-8', errors='ignore')

print("Output:\n", output)
print("Errors:\n", errors)

ssh.close()
