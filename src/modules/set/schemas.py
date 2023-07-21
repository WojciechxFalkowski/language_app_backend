from pydantic import BaseModel
from typing import List

from ..term.schemas import Term

class GetSet(BaseModel):
    id: int
    class Config():
        orm_mode = True

class CreateSet(BaseModel):
    name: str
    class Config():
        orm_mode = True

class Set(BaseModel):
    id: int
    name: str
    term_id: str
    user_id: str
    terms: List[Term]

    class Config():
        orm_mode = True

class ShowSet(BaseModel):
    id: int
    name: str
    # term_id: str
    user_id: str
    terms: List[Term]
    class Config():
        orm_mode = True

class DeleteSet(BaseModel):
    set_id: int
    class Config():
        orm_mode = True
