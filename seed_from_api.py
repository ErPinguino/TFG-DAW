import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import SessionLocal
from Services.game_service import import_game_from_rawg
from Models.game import GameORM

GAMES_TO_IMPORT = [
    "Elden Ring", "Cyberpunk 2077", "Hades", "The Witcher 3", "Red Dead Redemption 2",
    "Hollow Knight", "Baldur's Gate 3", "Stardew Valley", "Spider-Man 2", "God of War Ragnarok",
    "Grand Theft Auto V", "Skyrim", "Fallout 4", "Bloodborne", "Sekiro: Shadows Die Twice",
    "Dark Souls III", "Ghost of Tsushima", "Horizon Forbidden West", "Final Fantasy VII Rebirth",
    "Persona 5 Royal", "NieR: Automata", "Monster Hunter: World", "Mass Effect Legendary Edition",
    "Doom Eternal", "Resident Evil Village", "Alan Wake 2", "Minecraft", "Terraria",
    "Subnautica", "Left 4 Dead 2", "BioShock Infinite", "Borderlands 3", "Apex Legends",
    "Disco Elysium", "Outer Wilds", "Sea of Stars", "Cuphead", "Celeste", 
    "Ori and the Will of the Wisps", "Factorio", "RimWorld", "Dave the Diver",
    "Street Fighter 6", "Tekken 8", "Mortal Kombat 1", "Forza Horizon 5", 
    "Gran Turismo 7", "Rocket League", "FIFA 23", "NBA 2K24"
]

async def seed_catalog():
    load_dotenv()
    db = SessionLocal()
    
    print(f"🚀 Iniciando importación masiva de {len(GAMES_TO_IMPORT)} juegos...")
    print("-" * 60)

    contador_nuevos = 0
    contador_saltados = 0

    for game_name in GAMES_TO_IMPORT:
        try:
            exists = db.query(GameORM).filter(GameORM.title.ilike(f"%{game_name}%")).first()
            
            if not exists:
                # Importante: pasamos el db para que el service haga el commit
                game = await import_game_from_rawg(game_name, db)
                if game:
                    print(f"✅ Importado: {game.title}")
                    contador_nuevos += 1
                else:
                    print(f"⚠️ No encontrado en RAWG: {game_name}")
            else:
                print(f"⏩ Saltado: {game_name} (ya existe)")
                contador_saltados += 1
                
        except Exception as e:
            db.rollback() 
            print(f"❌ Error con '{game_name}': Ya existe o hubo un problema. Saltando...")

    db.close()
    print("-" * 60)
    print(f"✨ ¡Proceso terminado! Nuevos: {contador_nuevos} | Saltados: {contador_saltados}")

if __name__ == "__main__":
    asyncio.run(seed_catalog())