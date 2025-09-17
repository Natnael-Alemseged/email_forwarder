import time

from app.core.db import SessionLocal
from app.core.gmail_client import GmailClient
from app.model.rule import Rule
from app.service.email_service import save_sender_if_new

# from app.service.forwarder import forward_email  # your rule logic

client = GmailClient()


def check_inbox():
    db = SessionLocal()
    emails = client.fetch_unread()
    for mail in emails:
        sender = save_sender_if_new(db, mail["from"])

        # find matching rules for this sender
        rules = db.query(Rule).filter(Rule.sender_id == sender.id).all()
        for rule in rules:
            client.forward_email(
                original_sender=mail["from"],
                to_email=rule.user.email,  # user who subscribed
                subject=mail["subject"],
                body=mail["body"]
            )
    db.close()

def start_worker():
    while True:
        check_inbox()
        print("worker done cycle")
        time.sleep(10)  # poll every 30s
