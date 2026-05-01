from sqlalchemy.orm import Session
from Models.game import GameORM, GameBase, GameUpate

def get_all_games(db: Session):
    return db.query(GameORM).all()

def get_game_by_id(db: Session, game_id: int):
    return db.query(GameORM).filter(GameORM.id == game_id).first()

def create_game(db: Session, game_data: GameBase):
    new_game = GameORM(**game_data.model_dump())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

def update_game_stock(db: Session, game_id: int, new_stock: int):
    game = db.query(GameORM).filter(GameORM.id == game_id).first()
    if game:
        game.stock = new_stock
        db.commit()
        db.refresh(game)
    return game