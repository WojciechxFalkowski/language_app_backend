from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from ..sql_app.database import get_db

from . import schemas, service, models

router = APIRouter(tags=["Set"])

@router.post("/set")
def create_set(db_set = Depends(service.create_set)):
    try:
        print('db_set')
        print(db_set)
        return db_set
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sets",response_model=list[schemas.ShowSet])
def get_sets(sets = Depends(service.get_sets)):
    return sets 

@router.delete("/set/{set_id}", status_code=200, response_model=schemas.ShowSet)
def delete_set(set_id: int, db: Session = Depends(get_db)):
    try:
        db_set = db.query(models.Set).filter(models.Set.id == set_id).first()
        db.delete(db_set)
        db.commit()
        return db_set
    except Exception:
        raise HTTPException(status_code=404, detail="Set not found")

@router.get("/set/{set_id}", status_code=200, response_model=schemas.ShowSet)
def get_sets(set_id: int, db: Session = Depends(get_db)):
    set = db.query(models.Set).filter(models.Set.id == set_id).first()
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    return set