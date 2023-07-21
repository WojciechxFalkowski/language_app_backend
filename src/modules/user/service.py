from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from . import models, schemas
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from ..sql_app.database import get_db
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = models.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db,email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    print('get_current_active_user')
    # if current_user.disabled:
        # raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_user_by_email(db: Session, email: str):
    print('get_user_by_email')
    print(email)
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    print('get_user???')
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    print('create_user')
    try:
        hashed_password = get_password_hash(user.password)
        
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(models.User).filter_by(id=user_id).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")