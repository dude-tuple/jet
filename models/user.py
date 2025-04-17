__all__ = [
    'UserORM',
]

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .issue_assignee import issue_assignee


class UserORM(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # GitHub ID
    login = Column(String(100), unique=True, nullable=False)
    node_id = Column(String(100), nullable=False)
    avatar_url = Column(Text, nullable=True)
    gravatar_id = Column(String(100), nullable=True)
    type = Column(String(20), nullable=False)  # "User", "Organization", "Bot"
    site_admin = Column(Boolean, default=False)

    # one-to-many with Issue (issues created/submitted by user)
    issues: Mapped[list["IssueORM"]] = relationship(
        "IssueORM",
        back_populates="user"
    )

    # many-to-many with Issue
    issues_assigned: Mapped[list["IssueORM"]] = relationship(
        secondary=issue_assignee, back_populates="assignees"
    )

    # one-to-many with Repository
    repositories_owned: Mapped[list["RepositoryORM"]] = relationship(
        "RepositoryORM",
        back_populates="owner"
    )
