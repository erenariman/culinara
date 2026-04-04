from sqlalchemy import Column, String, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .base import Base

class SkillLevel(str, enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    website = Column(String, nullable=True)
    location = Column(String, nullable=True)
    skill_level = Column(SAEnum(SkillLevel), nullable=True)
    
    # Storing simple lists/dictionaries as Text/JSON is practical for MVP/Postgres
    dietary_restrictions = Column(Text, nullable=True) # JSON representation recommended
    preferences = Column(Text, nullable=True) # JSON representation recommended

    user = relationship("UserModel", back_populates="profile")
