from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # NEW or PROCESSED (we’ll keep it simple for now)
    status = Column(String(20), nullable=False, default="NEW")

    ai_summary = Column(Text, nullable=True)
    ai_priority = Column(String(10), nullable=True)  # LOW/MEDIUM/HIGH
    ai_draft_reply = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)