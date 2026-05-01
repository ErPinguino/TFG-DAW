from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from Models.order import OrderORM, OrderItemORM
from Models.cart import CartORM, CartItemORM
from Models.game import GameORM

def checkout(db: Session, user_id: int):
    cart = db.query(CartORM).filter(CartORM.user_id == user_id).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El carrito está vacío"
        )

    total_price = 0
    order_items_to_create = []

    for item in cart.items:
        game = db.query(GameORM).filter(GameORM.id == item.game_id).first()
        
        if not game:
            raise HTTPException(status_code=404, detail=f"Juego {item.game_id} no encontrado")

        if game.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {game.title}. Disponible: {game.stock}"
            )

        total_price += game.price * item.quantity
        
        new_order_item = OrderItemORM(
            game_id=game.id,
            quantity=item.quantity,
            price_at_purchase=game.price 
        )
        order_items_to_create.append((new_order_item, game))

    new_order = OrderORM(
        user_id=user_id,
        total_price=total_price,
        status="completed"
    )
    db.add(new_order)
    db.flush() 

    for order_item, game in order_items_to_create:
        order_item.order_id = new_order.id
        db.add(order_item)
        
        game.stock -= order_item.quantity

    db.query(CartItemORM).filter(CartItemORM.cart_id == cart.id).delete()

    db.commit()
    db.refresh(new_order)
    
    return new_order

def get_user_orders(db: Session, user_id: int):
    return db.query(OrderORM)\
        .options(joinedload(OrderORM.items).joinedload(OrderItemORM.game))\
        .filter(OrderORM.user_id == user_id)\
        .all()