from fastapi import FastAPI
from database import engine, Base
from Models import game, user 
from Routes import game_routes, user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameStore API",
    description="Backend del e-commerce de videojuegos",
    version="1.0.0"
)

app.include_router(game_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a GameStore! El servidor está vivo."}