__all__ = [
    'issue_label',
]

from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base


issue_label = Table(
    "issue_label",
    Base.metadata,
    Column("issue_id", Integer, ForeignKey("issue.id", ondelete="CASCADE"), primary_key=True),
    Column("label_id", Integer, ForeignKey("label.id", ondelete="CASCADE"), primary_key=True),
)
