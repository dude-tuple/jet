__all__ = [
    'RepositoryORM',
]

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text, DateTime
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from .user import UserORM
from utils import utcnow


class RepositoryORM(Base):
    __tablename__ = "repository"

    id = Column(Integer, primary_key=True)
    node_id = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False, unique=True)
    private = Column(Boolean, default=False)

    # FK to user (owner)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    owner: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="repositories_owned",
    )

    html_url = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    fork = Column(Boolean, default=False)
    homepage = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)
    forks_count = Column(Integer, default=0)
    stargazers_count = Column(Integer, default=0)
    watchers_count = Column(Integer, default=0)
    size = Column(Integer)
    default_branch = Column(String(100))
    open_issues_count = Column(Integer)

    topics = Column(JSONB, default=list)

    has_issues = Column(Boolean, default=True)
    has_projects = Column(Boolean, default=True)
    has_wiki = Column(Boolean, default=True)
    has_pages = Column(Boolean, default=False)
    has_discussions = Column(Boolean, nullable=True)
    archived = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    visibility = Column(String(20), default="public")

    pushed_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)

    allow_rebase_merge = Column(Boolean, nullable=True)
    squash_merge_allowed = Column(Boolean, nullable=True)
    allow_auto_merge = Column(Boolean, nullable=True)
    delete_branch_on_merge = Column(Boolean, nullable=True)
    allow_update_branch = Column(Boolean, nullable=True)
    use_squash_pr_title_as_default = Column(Boolean, nullable=True)
    is_template = Column(Boolean, default=False)
