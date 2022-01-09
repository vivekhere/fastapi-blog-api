from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: User

    class Config:
        orm_mode = True


class PostWithVotes(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    # dir: conint(ge=0, le=1)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
