__all__ = [
    'Reactions'
]

from typing import Optional

from pydantic import  Field

from pydantic import BaseModel


class Reactions(BaseModel):
    plus_one: Optional[int] = Field(0, alias="+1")
    minus_one: Optional[int] = Field(0, alias="-1")
    laugh: Optional[int] = 0
    confused: Optional[int] = 0
    heart: Optional[int] = 0
    rocket: Optional[int] = 0
    eyes: Optional[int] = 0
