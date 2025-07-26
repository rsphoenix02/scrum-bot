from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class StandupEntry(Base):
    __tablename__ = "standup_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Slack user ID
    channel_id = Column(String)
    yesterday = Column(String)
    today = Column(String)
    blockers = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
