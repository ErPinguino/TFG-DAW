import os
import httpx
from sqlalchemy.orm import Session
from Models.game import GameORM, GameBase, GameUpdate


RAWG_API_KEY = os.getenv("RAWG_API_KEY")

RAWG_API_KEY = os.getenv("RAWG_API_KEY")

async def import_game_from_rawg(game_name: str, db: Session):
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={game_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        if not data['results']:
            return None
        
        raw_game = data['results'][0]
        
        nuevo_juego = GameORM(
            title=raw_game['name'],
            price=59.99, 
            stock=10,
            genre=raw_game['genres'][0]['name'] if raw_game['genres'] else "Acción",
            platform=raw_game['platforms'][0]['platform']['name'] if raw_game['platforms'] else "PC",
            image_url=raw_game['background_image'] 
        )
        
        db.add(nuevo_juego)
        db.commit()
        db.refresh(nuevo_juego)
        return nuevo_juego

def get_all_games(
    db: Session, 
    page: int, 
    size: int, 
    genre: str = None, 
    platform: str = None, 
    search: str = None
):
    query = db.query(GameORM).filter(GameORM.is_active == True)

    traducciones_generos = {
        "acción": "Action",
        "accion": "Action",
        "rol": "RPG",
        "rpg": "RPG",
        "disparos": "Shooter",
        "estrategia": "Strategy",
        "indie": "Indie",
        "aventura": "Adventure",
        "carreras": "Racing",
        "deportes": "Sports",
        "lucha": "Fighting",
        "simulación": "Simulation",
        "simulacion": "Simulation"
    }

    if genre:
        genre_lower = genre.lower().strip()
        
        
        genre_filtrar = traducciones_generos.get(genre_lower, genre)
        
        query = query.filter(GameORM.genre.ilike(f"%{genre_filtrar}%"))
        
    if platform:
        query = query.filter(GameORM.platform.ilike(f"%{platform}%"))
        
    if search:
        query = query.filter(GameORM.title.ilike(f"%{search}%"))
    
    # 5. Lógica de Paginación (Offset y Limit)
    offset = (page - 1) * size
    
    # 6. Ejecutamos y devolvemos los resultados recortados
    return query.offset(offset).limit(size).all()

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

def delete_game(db: Session, game_id: int):
    db_game = db.query(GameORM).filter(GameORM.id == game_id).first()
    
    if db_game:
        db_game.is_active = False 
        db.commit()
        db.refresh(db_game)
        
    return db_game