import time
from app.core.gmail_client import GmailClient
# from app.service.forwarder import forward_email  # your rule logic

client = GmailClient()

def check_inbox():
    emails = client.fetch_unread()
    for mail in emails:
        print('mail is:',mail)
        # Here forward_email() decides who should get it based on rules
        client. forward_email(
            # sender=mail["from"],
            original_sender=mail['from'],
            to_email='natiaabaydam@gmail.com',
            subject=mail["subject"],
            body=mail["body"]
        )

def start_worker():
    while True:
        check_inbox()
        print("worker done cycle")
        time.sleep(5)  # poll every 30s
