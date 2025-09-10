import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
from app.core.db import SessionLocal
from app.model.rule import Rule
from app.model.user import User

# def forward_email(sender, subject, body):
#     db = SessionLocal()
#     # Match rules by sender domain
#     rules = db.query(Rule).filter(Rule.sender.in_([sender, sender.split("@")[-1]])).all()
#
#     if not rules:
#         return
#
#     smtp = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
#     smtp.starttls()
#     smtp.login(settings.GMAIL_USER, settings.GMAIL_PASSWORD)
#
#     for rule in rules:
#         user = db.query(User).filter(User.id == rule.user_id).first()
#         if user:
#             msg = MIMEText(body)
#             msg["Subject"] = f"[FWD] {subject} (from {sender})"
#             msg["From"] = settings.GMAIL_USER
#             msg["To"] = user.email
#             smtp.sendmail(settings.GMAIL_USER, user.email, msg.as_string())
#
#     smtp.quit()
#     db.close()
