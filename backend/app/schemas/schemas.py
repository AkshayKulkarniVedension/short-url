from pydantic import BaseModel

class URLBase(BaseModel):
    original_url: str

class URLCreate(URLBase):
    pass

class URLDisplay(URLBase):
    id: int
    short_url: str

    class Config:
        orm_mode = True

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
