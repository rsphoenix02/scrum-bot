from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
# from app.models.user import User

class StandupEntry(Base):
    __tablename__ = "standup_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"))
    yesterday = Column(String)
    today = Column(String)
    blockers = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="standups")
