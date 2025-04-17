__all__ = [
    'Issue',
]

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from .label import Label
from .reactions import Reactions
from .user import User


class Issue(BaseModel):
    id: int
    node_id: str
    number: int
    title: str
    body: Optional[str] = None
    user: User
    labels: List[Label] = []
    state: str
    locked: bool
    assignee: Optional[User] = None
    assignees: List[User] = []
    milestone: Optional[dict] = None
    comments: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    author_association: Optional[str] = None
    active_lock_reason: Optional[str] = None
    reactions: Reactions
    timeline_url: HttpUrl
    performed_via_github_app: Optional[dict] = None
    state_reason: Optional[str] = None
