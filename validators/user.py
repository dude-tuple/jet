__all__ = [
    'User'
]

from typing import Optional

from pydantic import BaseModel, HttpUrl


class User(BaseModel):
    id: int
    login: str
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: Optional[str] = None
    type: str
    site_admin: bool
