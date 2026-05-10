from sqlalchemy.orm import Session
from Models.cart import CartORM, CartItemORM
from Models.game import GameORM

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(CartORM).filter(CartORM.user_id == user_id).first()
    if not cart:
        cart = CartORM(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_item_to_cart(db: Session, user_id: int, game_id: int, quantity: int):
    cart = get_or_create_cart(db, user_id)
    
    item = db.query(CartItemORM).filter(
        CartItemORM.cart_id == cart.id, 
        CartItemORM.game_id == game_id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItemORM(cart_id=cart.id, game_id=game_id, quantity=quantity)
        db.add(item)
    
    db.commit()
    db.refresh(cart)
    return cart

def get_cart_total(cart: CartORM):
    return sum(item.game.price * item.quantity for item in cart.items)

def remove_item_from_cart(db: Session, user_id: int, game_id: int):
    cart = db.query(CartORM).filter(CartORM.user_id == user_id).first()
    if not cart:
        return None

    item = db.query(CartItemORM).filter(
        CartItemORM.cart_id == cart.id, 
        CartItemORM.game_id == game_id
    ).first()

    if item:
        db.delete(item)
        db.commit()
    return cart

def clear_cart(db: Session, user_id: int):
    cart = db.query(CartORM).filter(CartORM.user_id == user_id).first()
    if cart:
        db.query(CartItemORM).filter(CartItemORM.cart_id == cart.id).delete()
        db.commit()
    return cart