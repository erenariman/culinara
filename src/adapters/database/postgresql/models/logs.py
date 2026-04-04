from sqlalchemy import Column, String, Text, ForeignKey, Enum as SAEnum, DateTime, func
from sqlalchemy.orm import relationship
import enum

from .base import Base
from .social import EntityType # Reuse existing Enum

class ModerationAction(str, enum.Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    DELETE = "DELETE"

class ModerationLogModel(Base):
    __tablename__ = "moderation_logs"

    id = Column(String, primary_key=True, index=True)
    target_type = Column(SAEnum(EntityType), nullable=False)
    target_id = Column(String, nullable=False)
    moderator_id = Column(String, ForeignKey("users.id"), nullable=False)
    action = Column(SAEnum(ModerationAction), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SearchLogModel(Base):
    __tablename__ = "search_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    query_text = Column(String, nullable=False)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())
