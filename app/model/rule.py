from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)  # e.g., netflix.com
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="rules")