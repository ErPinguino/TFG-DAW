import jwt
import os 
from datetime import datetime, timedelta, timezone # Añadimos timezone para Python moderno
from dotenv import load_dotenv 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRY_VAR = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if not SECRET_KEY or not ALGORITHM or not EXPIRY_VAR:
    raise RuntimeError("❌ ERROR: Faltan variables de entorno en el archivo .env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(EXPIRY_VAR)

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o caducado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(payload.get("sub")) 