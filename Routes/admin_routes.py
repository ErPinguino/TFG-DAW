from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Services import admin_service
from Services.auth_service import get_current_user
from Models.user import UserORM

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)

@router.get("/dashboard")
def read_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado. Se requieren permisos de administrador."
        )
        
    return admin_service.get_dashboard_stats(db)