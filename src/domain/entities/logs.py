from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from .social import EntityType

class ModerationAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    DELETE = "DELETE"

@dataclass
class ModerationLog:
    id: str
    target_type: EntityType
    target_id: str
    moderator_id: str
    action: ModerationAction
    reason: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class SearchLog:
    id: str
    query_text: str
    user_id: Optional[str] = None
    searched_at: datetime = field(default_factory=datetime.now)
