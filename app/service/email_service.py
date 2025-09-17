# app/services/email_service.py
from sqlalchemy.orm import Session
from app.model.sender import Sender
import re

import email.utils

def save_sender_if_new(db: Session, sender_email: str):
    name, addr = email.utils.parseaddr(sender_email)
    sender = db.query(Sender).filter_by(email=addr).first()
    if not sender:
        sender = Sender(email=addr, name=name or None)
        db.add(sender)
        db.commit()
        db.refresh(sender)
    return sender
