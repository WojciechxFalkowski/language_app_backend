from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from ..sql_app.database import get_db
from ..user.service import get_current_user
from ..user.models import User

from ..set.models import Set
from ..set.service import get_set_by_id

from . import models, schemas

def create_term(term: schemas.CreateTerm, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        current_set: Set = get_set_by_id(term.set_id, current_user, db),

        db_set = models.Term(question=term.question,answer=term.answer,positive_points=term.positive_points,negative_points=term.negative_points, set_id=current_set[0].id)
        db.add(db_set)
        db.commit()
        db.refresh(db_set)
        print('db_set')

        return db_set
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_term(term: schemas.UpdateTerm, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_set: Set = get_set_by_id(term.set_id, current_user, db)
    # db_set = models.Term(question=term.question,answer=term.answer,positive_points=term.positive_points,negative_points=term.negative_points, set_id=current_set[0].id)
    for db_term in current_set.terms:
            if db_term.id == term.id:
                # print("db_term")
                # print(db_term.answer)
                db_term.question = term.question
                db_term.answer = term.answer
                db_term.positive_points = term.positive_points
                db_term.negative_points = term.negative_points
                # question=term.question,answer=term.answer,positive_points=term.positive_points,negative_points=term.negative_points
                # db.
                # db.delete(db_term)
                db.commit()
                print(db_term.answer)
                return db_term
    # db.add(db_set)
    # db.commit()
    # db.refresh(db_set)
    # print('db_set')

    # return db_set

def delete_term(term: schemas.DeleteTerm, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # print('delete_term')
    # print(term)
    try:
        current_set: Set = get_set_by_id(term.set_id, current_user, db)
        # print('current_set')
        # print(current_set)
        # print(current_set.id)
        for db_term in current_set.terms:
            if db_term.id == term.id:
                print("db_term")
                print(db_term)
                db.delete(db_term)
                db.commit()
                return db_term
        raise HTTPException(status_code=404, detail="Term not found")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=404, detail="Term not found")

def get_terms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Term).filter(Set.user_id == current_user.id).all()