from pydantic import BaseModel
import datetime as _datetime

class UserBase(BaseModel):
    username : str
    email : str
    group : str

class UserRequest(UserBase):
    password: str

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: _datetime.datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    text: str
    post_title: str

class PostRequest(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_by: int
    created_at: _datetime.datetime

    class Config:
        orm_mode = True