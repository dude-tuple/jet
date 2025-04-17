__all__ = [
    'issue_assignee',
]

from sqlalchemy import Column, ForeignKey, Table

from .base import Base


issue_assignee = Table(
    "issue_assignee",
    Base.metadata,
    Column("issue_id", ForeignKey("issue.id")),
    Column("assignee_id", ForeignKey("user.id")),
)
