from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import schemas, service, models
from ..sql_app.database import get_db
from datetime import datetime, timedelta
from email_validator import validate_email

ACCESS_TOKEN_EXPIRE_MINUTES = 3000000
router = APIRouter(tags=["User"])

@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    try:
        user = service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise Exception("Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(service.get_current_active_user)):
    return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_users(db, skip=skip, limit=limit)

@router.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = service.get_user_by_email(db, email=user.email)
        if db_user:
            raise Exception("Email already registered")
    # raise HTTPException(status_code=400, detail="error")
        # validate_email(user.email)
        return service.create_user(db=db, user=user)
    except Exception as e:
        print('except')
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return service.delete_user(db, user_id = user_id)




# @router.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return service.create_user_item(db=db, item=item, user_id=user_id)


# @router.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = service.get_items(db, skip=skip, limit=limit)
#     return items


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}