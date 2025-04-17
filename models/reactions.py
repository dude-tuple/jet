__all__ = [
    "ReactionsORM"
]

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import  relationship

from models import Base


class ReactionsORM(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True)

    issue_id = Column(Integer, ForeignKey("issue.id", ondelete="CASCADE"), unique=True, nullable=False)
    issue = relationship("IssueORM", back_populates="reactions", uselist=False, single_parent=True)

    plus_one = Column(Integer, default=0)
    minus_one = Column(Integer, default=0)
    laugh = Column(Integer, default=0)
    confused = Column(Integer, default=0)
    heart = Column(Integer, default=0)
    rocket = Column(Integer, default=0)
    eyes = Column(Integer, default=0)
