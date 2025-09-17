# app/model/sender.py
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class Sender(Base):
    __tablename__ = "senders"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    rules = relationship("Rule", back_populates="sender")
