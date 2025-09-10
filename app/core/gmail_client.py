import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from typing import List, Dict
from app.core.config import settings


class GmailClient:
    def __init__(self):
        self.imap_server = settings.IMAP_SERVER
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.user = settings.GMAIL_USER
        self.password = settings.GMAIL_PASSWORD

    # -------------------
    # Fetch unread emails
    # -------------------
    def fetch_unread(self) -> List[Dict]:
        print("🔍 Connecting to IMAP server...")
        messages = []

        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.user, self.password)
        print("✅ Logged in to IMAP")

        mail.select("inbox")
        print("📥 Inbox selected")

        status, data = mail.search(None, "UNSEEN")
        print(f"🔎 Search status: {status}, Data: {data}")

        if status != "OK":
            print("⚠️ No unread emails found")
            mail.logout()
            return messages

        for num in data[0].split():
            print(f"➡️ Fetching message ID: {num.decode()}")
            _, msg_data = mail.fetch(num, "(RFC822)")
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            sender = msg["From"]
            subject = msg["Subject"]
            print(f"📧 From: {sender}, Subject: {subject}")

            # Extract body
            body = ""
            if msg.is_multipart():
                print("📑 Message is multipart")
                for part in msg.walk():
                    content_type = part.get_content_type()
                    print(f"   🔹 Part content type: {content_type}")
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        print("   ✅ Found plain text body")
                        break
                    elif content_type == "text/html" and not body:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        print("   ✅ Found HTML body as fallback")
            else:
                print("📄 Message is single-part")
                body = msg.get_payload(decode=True).decode(errors="ignore")

            print(f"📝 Extracted body (first 100 chars): {body[:100]}...")

            messages.append({
                "id": num.decode(),
                "from": sender,
                "subject": subject,
                "body": body
            })

            # Mark as seen
            mail.store(num, '+FLAGS', '\\Seen')
            print(f"✔️ Marked message {num.decode()} as seen")

        mail.logout()
        print("🔒 Logged out from IMAP")
        return messages

    # -------------------
    # Forward email
    # -------------------
    def forward_email(self, to_email: str, subject: str, body: str, original_sender: str):
        print(f"🚀 Forwarding email to {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Original sender: {original_sender}")
        print(f"   Body (first 100 chars): {body[:100]}...")

        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        print("🔌 Connected to SMTP server")

        smtp.starttls()
        print("🔐 Started TLS")

        smtp.login(self.user, self.password)
        print("✅ Logged in to SMTP")

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = f"[FWD] {subject} (from {original_sender})"
        msg["From"] = self.user
        msg["To"] = to_email

        smtp.sendmail(self.user, [to_email], msg.as_string())
        print("📤 Email sent successfully!")

        smtp.quit()
        print("🔒 Logged out from SMTP")
