from pydantic import BaseModel

class Term(BaseModel):
    id: int
    question: str
    answer: str
    positive_points: int
    negative_points: int
    set_id: int
    class Config():
        orm_mode = True

class CreateTerm(BaseModel):
    set_id: str
    question: str
    answer: str
    positive_points: int
    negative_points: int
    
    class Config():
        orm_mode = True

class DeleteTerm(BaseModel):
    set_id: int
    id: int    
    class Config():
        orm_mode = True

class UpdateTerm(BaseModel):
    set_id: int
    id: int
    question: str
    answer: str
    positive_points: int
    negative_points: int

    class Config():
        orm_mode = True