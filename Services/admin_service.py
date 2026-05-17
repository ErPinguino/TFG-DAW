from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.user import UserORM
from Models.game import GameORM
from Models.order import OrderORM 

def get_dashboard_stats(db: Session):
    total_users = db.query(UserORM).count()
    total_games_in_catalog = db.query(GameORM).filter(GameORM.is_active == True).count()
    
    low_stock_games = db.query(GameORM).filter(GameORM.is_active == True, GameORM.stock < 3).all()
    low_stock_list = [{"id": g.id, "title": g.title, "stock": g.stock} for g in low_stock_games]
    
    total_inventory_value = db.query(func.sum(GameORM.price * GameORM.stock)).filter(GameORM.is_active == True).scalar() or 0.0
    
    total_earnings = db.query(func.sum(OrderORM.total_price)).scalar() or 0.0

    return {
        "total_users": total_users,
        "total_games_in_catalog": total_games_in_catalog,
        "total_inventory_value": round(total_inventory_value, 2),
        "total_earnings": round(total_earnings, 2), 
        "low_stock_alerts_count": len(low_stock_list),
        "low_stock_games": low_stock_list
    }