__all__ = [
    'Label'
]

from typing import Optional

from pydantic import BaseModel


class Label(BaseModel):
    id: int
    node_id: str
    name: str
    color: str
    default: Optional[bool] = None
