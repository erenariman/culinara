from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SAEnum, DateTime, func
from sqlalchemy.orm import relationship
import enum

from .base import Base

class EntityType(str, enum.Enum):
    RECIPE = "RECIPE"
    COMMENT = "COMMENT"
    USER = "USER"

class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=False)
    text = Column(Text, nullable=False)
    parent_id = Column(String, ForeignKey("comments.id"), nullable=True) # Threading
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Soft Delete

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=False)
    rating = Column(Integer, nullable=False) # 1-5
    text = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FollowModel(Base):
    __tablename__ = "follows"

    follower_id = Column(String, ForeignKey("users.id"), primary_key=True)
    following_id = Column(String, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BlockModel(Base):
    __tablename__ = "blocks"

    blocker_id = Column(String, ForeignKey("users.id"), primary_key=True)
    blocked_id = Column(String, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    reporter_id = Column(String, ForeignKey("users.id"), nullable=False)
    target_type = Column(SAEnum(EntityType), nullable=False)
    target_id = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(SAEnum(ReportStatus), default=ReportStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RecipeLikeModel(Base):
    __tablename__ = "recipe_likes"
    
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    recipe_id = Column(String, ForeignKey("recipes.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
