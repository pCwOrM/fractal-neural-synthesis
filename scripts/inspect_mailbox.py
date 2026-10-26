import imaplib
import email
from email.header import decode_header
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def clean_header(val):
    if not val:
        return ""
    try:
        decoded = decode_header(val)
        res = []
        for text, enc in decoded:
            if isinstance(text, bytes):
                try:
                    res.append(text.decode(enc or "utf-8", errors="replace"))
                except Exception:
                    res.append(text.decode("latin1", errors="replace"))
            else:
                res.append(str(text))
        return "".join(res)
    except Exception:
        return str(val)

try:
    M = imaplib.IMAP4_SSL("mail.answerr.me", 993, timeout=10)
    M.login("ask@answerr.me", "Jesmaat.19")

    typ, mailboxes = M.list()
    print("=== Mailboxes ===")
    folder_names = []
    for mb in mailboxes:
        decoded_mb = mb.decode("latin1", errors="replace")
        print("  ", decoded_mb)
        # Parse mailbox name: typically '(\\HasNoChildren) "/" "INBOX"'
        parts = decoded_mb.split(' "/" ')
        if len(parts) == 2:
            name = parts[1].strip('"')
            folder_names.append(name)

    for folder in folder_names:
        try:
            res, count = M.select(f'"{folder}"', readonly=True)
            if res != "OK":
                continue
            typ, data = M.search(None, "ALL")
            msg_ids = data[0].split()
            print(f"\n==========================================")
            print(f" Folder: {folder} (Total: {len(msg_ids)} messages)")
            print(f"==========================================")
            # Read last 15 messages
            for mid in msg_ids[-15:]:
                typ, mdata = M.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM TO CC BCC SUBJECT DATE)])")
                if not mdata or not mdata[0]:
                    continue
                raw_header = mdata[0][1].decode("latin1", errors="replace")
                msg = email.message_from_string(raw_header)
                d = msg.get("Date", "")
                f = clean_header(msg.get("From", ""))
                t = clean_header(msg.get("To", ""))
                s = clean_header(msg.get("Subject", ""))
                print(f"ID {mid.decode():<4} | Date: {d[:25]:<25} | From: {f[:35]:<35} | To: {t[:30]:<30} | Subj: {s}")
        except Exception as e:
            print(f"Error checking folder {folder}: {e}")

    M.logout()
except Exception as e:
    print(f"Fatal error: {e}")
