from sqlalchemy.orm import Session
from . import models, schemas
from ..sql_app.database import get_db
from fastapi import Depends
from ..user.service import get_current_user 
from ..user.models import User
from fastapi import Depends, HTTPException

def create_set(set: schemas.CreateSet, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_set = models.Set(name=set.name,user_id=current_user.id)
        db.add(db_set)
        db.commit()
        db.refresh(db_set)
        return db_set
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_sets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Set).filter(models.Set.user_id == current_user.id).all()

def get_set(set_id: int = 1, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Set).all()

def get_set_by_id(set_id: int, current_user: User, db: Session):
    return db.query(models.Set).filter(models.Set.user_id == current_user.id).filter(models.Set.id == set_id).first()
