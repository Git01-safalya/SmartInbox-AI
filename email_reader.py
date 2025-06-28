import imaplib
import email
from email.header import decode_header
import subprocess

def clean(text):
    return "".join(c if c.isprintable() else " " for c in text)

def fetch_emails(username, app_password, count=5):
    """Fetches UNREAD emails from Gmail using IMAP."""
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, app_password)
    imap.select("inbox")

    # 🔄 1️⃣‑‑> only unread messages
    status, messages = imap.search(None, "UNSEEN")

    email_ids = messages[0].split()[-count:]
    emails = []

    for eid in reversed(email_ids):
        _, msg_data = imap.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["subject"] or "No Subject"
                subject = decode_header(subject)[0][0]
                subject = subject.decode() if isinstance(subject, bytes) else subject

                # get plain‑text body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset() or "utf-8"
                            body = part.get_payload(decode=True).decode(charset, errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                emails.append(
                    {"subject": clean(subject), "body": clean(body)}
                )

        # ✅ 2️⃣‑‑> mark as read so it won’t re‑appear next time
        imap.store(eid, "+FLAGS", "\\Seen")

    imap.logout()
    return emails



def summarize_with_agent(email_text: str):
    prompt = f"""
You are an assistant that helps summarize emails.

TASK:
1. Summarize the email in 2 lines.
2. List action items as bullet points.
3. Suggest if a follow-up is needed.

EMAIL:
\"\"\"
{email_text}
\"\"\"
"""
    process = subprocess.Popen(
        ["ollama", "run", "granite3.2:8b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    output, error = process.communicate(input=prompt)
    return output.strip()
