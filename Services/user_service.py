from sqlalchemy.orm import Session
from Models.user import UserORM, UserBase
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(UserORM).filter(UserORM.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(UserORM).filter(UserORM.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserORM).filter(UserORM.id == user_id).first()

def create_user(db: Session, user_data: UserBase):
    db_user = get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya está registrado en nuestra base de datos."
        )
    
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )

    hashed_pwd = pwd_context.hash(user_data.password)
    
    new_user = UserORM(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)