from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Badge:
    id: str
    name: str
    icon_url: str
    description: str

@dataclass
class UserBadge:
    user_id: str
    badge_id: str
    earned_at: datetime = field(default_factory=datetime.now)
    # Optional full badge object if joined
    badge: Optional[Badge] = None

@dataclass
class Level:
    level: int
    xp_required: int
    title: str

@dataclass
class CookLog:
    id: str
    user_id: str
    recipe_id: str
    cooked_at: datetime = field(default_factory=datetime.now)
    rating: Optional[int] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None
