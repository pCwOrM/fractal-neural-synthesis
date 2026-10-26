import imaplib
import email
from email.header import decode_header
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                except Exception:
                    return str(part.get_payload())
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == 'text/html':
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                except Exception:
                    return str(part.get_payload())
    else:
        try:
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace')
        except Exception:
            return str(msg.get_payload())
    return ""

M = imaplib.IMAP4_SSL("mail.answerr.me", 993, timeout=10)
M.login("ask@answerr.me", "Jesmaat.19")
M.select("INBOX", readonly=True)

target_ids = ["49", "51", "52", "53", "54", "56", "57", "58", "59"]

for mid in target_ids:
    typ, data = M.fetch(mid, "(RFC822)")
    if not data or not data[0]:
        continue
    raw = data[0][1]
    msg = email.message_from_bytes(raw)
    print(f"\n=======================================================")
    print(f"MESSAGE ID: {mid}")
    print(f"From: {msg.get('From')}")
    print(f"To: {msg.get('To')}")
    print(f"Date: {msg.get('Date')}")
    print(f"Subject: {msg.get('Subject')}")
    print(f"------------------- BODY PREVIEW ----------------------")
    body = get_body(msg)
    print(body[:1500])
    print(f"=======================================================\n")

M.logout()
