from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    """Schema representation of a Post"""

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """Schema representation for creating a post"""


class PostUpdate(PostBase):
    """Schema representation for updating a post"""

    published: bool


class Post(PostBase):
    """Schema representation for the response Post"""

    id: int
    created: datetime

    class Config:
        orm_mode = True
