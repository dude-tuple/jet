__all__ = [
    'LabelORM',
]
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from .issue_label import issue_label


class LabelORM(Base):
    __tablename__ = "label"

    id = Column(Integer, primary_key=True)
    node_id = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(20), nullable=False)
    default = Column(Boolean, nullable=True)

    issues: Mapped[list["IssueORM"]] = relationship(
        "IssueORM",
        secondary=issue_label,
        back_populates="labels"
    )
