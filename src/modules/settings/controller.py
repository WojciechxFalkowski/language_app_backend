from fastapi import Depends, APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..sql_app.database import get_db
from . import schemas, service
router = APIRouter(tags=["Settings"])
from typing import List

@router.get("/settings",response_model=List[schemas.Setting])
def get_settings(db_settings = Depends(service.get_settings)):
    return db_settings

@router.post("/settings",response_model=List[schemas.Setting])
def create_setting(db_settings = Depends(service.create_settings)):
    return db_settings

@router.put("/settings/level/{level_id}", response_model=List[schemas.Setting])
def change_level(db_settings = Depends(service.change_level)):
    try:
      return db_settings
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))  