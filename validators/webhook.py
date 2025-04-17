__all__ = [
    'GitHubWebhook'
]

from pydantic import BaseModel

from .issue import Issue
from .repository import Repository
from .user import User


class GitHubWebhook(BaseModel):
    action: str
    issue: Issue
    repository: Repository
    sender: User
