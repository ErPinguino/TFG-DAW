from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Models.game import GameBase, GameResponse
from Services import game_service
from typing import List

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

@router.get("/", response_model=List[GameResponse])
def read_games(db: Session = Depends(get_db)):
    return game_service.get_all_games(db)

@router.get("/{game_id}", response_model=GameResponse)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = game_service.get_game_by_id(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return db_game

@router.post("/", response_model=GameResponse)
def create_game(game: GameBase, db: Session = Depends(get_db)):
    return game_service.create_game(db, game)