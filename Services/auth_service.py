import jwt
import os 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from passlib.context import CryptContext 

from Services import user_service
from database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRY_VAR = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if not SECRET_KEY or not ALGORITHM or not EXPIRY_VAR:
    raise RuntimeError("❌ ERROR: Faltan variables de entorno en el archivo .env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(EXPIRY_VAR)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username_or_email: str, password: str):
    user = user_service.get_user_by_username(db, username=username_or_email)
    
    if not user:
        user = user_service.get_user_by_email(db, email=username_or_email)
        
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user 


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.PyJWTError):
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o caducado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(payload.get("sub")) 

def get_current_user(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    user = user_service.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    return user