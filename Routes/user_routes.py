from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from Models.user import UserBase, UserPublicResponse
from Services import user_service

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/register", response_model=UserPublicResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserBase, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return user_service.create_user(db, user)

@router.post("/login")
def login(user_credentials: UserBase, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, user_credentials.email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    is_valid = user_service.verify_password(user_credentials.password, user.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {"mensaje": "Login exitoso", "username": user.username}