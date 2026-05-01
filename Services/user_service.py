from sqlalchemy.orm import Session
from Models.user import UserORM, UserBase
import bcrypt

def get_user_by_email(db: Session, email: str):
    return db.query(UserORM).filter(UserORM.email == email).first()

def create_user(db: Session, user_data: UserBase):
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(user_data.password.encode('utf-8'), salt)
    
    new_user = UserORM(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd.decode('utf-8')
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )