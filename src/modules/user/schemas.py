from pydantic import BaseModel
from typing import List

import datetime

class UserBase(BaseModel):
    email: str
    class Config():
        orm_mode = True

class UserCreate(UserBase):
    password: str

    class Config():
        orm_mode = True

class User(UserBase):
    id: int
    email: str #EmailStr
    created_date: datetime.datetime
    updated_at: datetime.datetime

    class Config():
        orm_mode = True
