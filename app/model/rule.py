# app/model/rule.py
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Rule(Base):
    __tablename__ = "rules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String, ForeignKey("senders.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="rules")
    sender = relationship("Sender", back_populates="rules")
