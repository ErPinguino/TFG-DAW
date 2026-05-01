from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Models.cart import CartResponse, CartItemBase
from Services import cart_service

router = APIRouter(prefix="/cart", tags=["Carrito"])

from Services.auth_service import get_current_user_id

@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
):
    cart = cart_service.get_or_create_cart(db, user_id)
    total = cart_service.get_cart_total(cart)
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": cart.items,
        "total_price": total
    }

@router.post("/add")
def add_to_cart(
    item_data: CartItemBase, 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id) # <--- Seguridad total
):
    return cart_service.add_item_to_cart(db, user_id, item_data.game_id, item_data.quantity)
    
@router.delete("/remove/{game_id}")
def remove_item(game_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    cart = cart_service.remove_item_from_cart(db, user_id, game_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return {"mensaje": "Juego eliminado del carrito"}

@router.delete("/clear")
def clear_cart(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
               ):
    cart_service.clear_cart(db, user_id)
    return {"mensaje": "Carrito vaciado correctamente"}