from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List

class EntityType(str, Enum):
    RECIPE = "RECIPE"
    COMMENT = "COMMENT"
    USER = "USER"

class ReportStatus(str, Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

@dataclass
class Comment:
    id: str
    user_id: str
    recipe_id: str
    text: str
    parent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    # For threading
    replies: List['Comment'] = field(default_factory=list)

@dataclass
class Review:
    id: str
    user_id: str
    recipe_id: str
    rating: int  # 1-5
    text: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Follow:
    follower_id: str
    following_id: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Block:
    blocker_id: str
    blocked_id: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Report:
    id: str
    reporter_id: str
    target_type: EntityType
    target_id: str
    reason: str
    status: ReportStatus = ReportStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
