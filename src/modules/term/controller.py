from fastapi import Depends, APIRouter
from . import service
from fastapi import Depends, HTTPException

router = APIRouter(tags=["Term"])

@router.post("/term")
def create_term(db_term = Depends(service.create_term)):
    try:
        return db_term
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/term")
def update_term(db_term = Depends(service.update_term)):
    return db_term

@router.delete("/term")
def delete_term(db_term = Depends(service.delete_term)):
    return db_term    

@router.get("/terms")
def get_terms(terms = Depends(service.get_terms)):
    return terms
