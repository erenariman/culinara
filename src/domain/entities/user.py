from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

class SkillLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

@dataclass
class UserProfile:
    user_id: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    skill_level: Optional[SkillLevel] = None
    dietary_restrictions: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class User:
    id: str
    email: str
    username: str
    is_active: bool = True
    slug: str = ""
    is_superuser: bool = False
    hashed_password: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    profile: Optional[UserProfile] = None
