from pydantic import BaseModel, EmailStr
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


class UserBase(BaseModel):
    """Schema representation for base user pydantic model"""

    email: EmailStr


class UserCreate(UserBase):
    """Schema representation for creating a user"""
    password: str


class UserRead(UserBase):
    """Schema representation for the User response model"""

    id: int
    created: datetime

    class Config:
        orm_mode = True
