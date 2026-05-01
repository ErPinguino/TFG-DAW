from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from Services import order_service
from Services.auth_service import get_current_user
from Models.user import UserORM
from Models.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["Pedidos"])

@router.post("/checkout", response_model=OrderResponse)
def create_order(
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
   
    return order_service.checkout(db, current_user.id)

@router.get("/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
   
    return order_service.get_user_orders(db, current_user.id)