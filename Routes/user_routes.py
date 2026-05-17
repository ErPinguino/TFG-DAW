from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db

from Models.user import (
    UserBase,
    UserPublicResponse,
    UserORM
)

from Services import user_service
from Services import auth_service
from Services.auth_service import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# =========================
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=UserPublicResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserBase,
    db: Session = Depends(get_db)
):

    db_user = user_service.get_user_by_email(
        db,
        email=user.email
    )

    if db_user:

        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    return user_service.create_user(
        db,
        user
    )

# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = auth_service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# =========================
# PERFIL USUARIO ACTUAL
# =========================

@router.get(
    "/me",
    response_model=UserPublicResponse
)
def get_me(
    current_user: UserORM = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }