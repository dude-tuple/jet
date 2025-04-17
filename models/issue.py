__all__ = [
    'issue_assignee',
    'IssueORM'
]

from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from .issue_assignee import issue_assignee
from .issue_label import issue_label
from .user import UserORM

from utils import utcnow


class IssueORM(Base):
    __tablename__ = "issue"

    id = Column(Integer, primary_key=True)
    node_id = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    body = Column(Text)

    # Foreign key to issue author - many-to-one
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    user = relationship("UserORM", back_populates="issues")

    state = Column(String(20), nullable=False)
    locked = Column(Boolean, default=False)

    comments = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow)
    closed_at = Column(DateTime, nullable=True)

    author_association = Column(String(100), nullable=True)
    active_lock_reason = Column(String(255), nullable=True)
    timeline_url = Column(Text, nullable=False)
    state_reason = Column(String(100), nullable=True)

    milestone = Column(JSONB, nullable=True)
    performed_via_github_app = Column(Boolean, nullable=True)

    # One-to-one relationship with Reaction
    reactions = relationship("ReactionsORM", back_populates="issue")

    # Many-to-many with User (User as Assignee)
    assignees: Mapped[List["UserORM"]] = relationship(
        secondary=issue_assignee, back_populates="issues_assigned"
    )

    # Many-to-many with Label
    labels: Mapped[list["LabelORM"]] = relationship(
        "LabelORM",
        secondary=issue_label,
        back_populates="issues"
    )
