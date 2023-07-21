from pydantic import BaseModel
from typing import List

class Level(BaseModel):
    id:int
    label:str
    is_selected:bool
    setting_id: int
    class Config():
        orm_mode = True

class Setting(BaseModel):
    id: int
    label: str
    options: List[Level]
    user_id: int
    class Config():
        orm_mode = True

class CreateSetting(BaseModel):
    label: str
    options: List[Level]
    class Config():
        orm_mode = True