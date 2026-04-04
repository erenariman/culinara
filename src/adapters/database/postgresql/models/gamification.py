from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, func
from .base import Base

class CookLogModel(Base):
    __tablename__ = "cook_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=False)
    cooked_at = Column(DateTime(timezone=True), server_default=func.now())
    rating = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    photo_url = Column(String, nullable=True)

class LevelModel(Base):
    __tablename__ = "levels"

    level = Column(Integer, primary_key=True)
    xp_required = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

class BadgeModel(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    icon_url = Column(String, nullable=False)
    description = Column(Text, nullable=False)

class UserBadgeModel(Base):
    __tablename__ = "user_badges"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    badge_id = Column(String, ForeignKey("badges.id"), primary_key=True)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
