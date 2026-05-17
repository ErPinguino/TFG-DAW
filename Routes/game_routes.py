from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Services.auth_service import get_current_user
from database import get_db
from Models.game import GameBase, GameResponse
from Models.user import UserORM
from Services import game_service
from typing import List, Optional

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

@router.get("/", response_model=List[GameResponse])
def read_games(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(12, ge=1, le=50, description="Juegos por página"),
    genre: Optional[str] = Query(None, description="Filtrar por género"),
    platform: Optional[str] = Query(None, description="Filtrar por plataforma"),
    search: Optional[str] = Query(None, description="Buscar por título o nombre"),
    db: Session = Depends(get_db)
):
    # Pasamos todos los filtros y la paginación al servicio
    return game_service.get_all_games(
        db, page=page, size=size, genre=genre, platform=platform, search=search
    )

@router.get("/{game_id}", response_model=GameResponse)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_service.get_game_by_id(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return db_game

@router.post("/", response_model=GameResponse)
def create_game(
    game: GameBase, 
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user) # <-- Añadido para control de roles
):
    # Ahora nadie puede inventarse un juego a mano si no es administrador
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, 
            detail="Operación no permitida. Se requieren permisos de administrador."
        )
    return game_service.create_game(db, game)

@router.post("/import/{name}", response_model=GameResponse)
async def import_game(
    name: str, 
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user) 
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, 
            detail="Operación no permitida. Se requieren permisos de administrador."
        )
    
    return await game_service.import_game_from_rawg(name, db)

@router.delete("/{game_id}", response_model=GameResponse)
def delete_game(
    game_id: int, 
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permisos insuficientes.")
        
    db_game = game_service.delete_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
        
    return db_game