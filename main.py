from fastapi import FastAPI
from database import engine, Base
from Models import game, user 
from Routes import game_routes, user_routes, cart_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GameStore API",
    description="Backend del e-commerce de videojuegos",
    version="1.0.0"
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

Base.metadata.create_all(bind=engine)


app.include_router(game_routes.router)
app.include_router(user_routes.router)
app.include_router(cart_routes.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a GameStore! El servidor está vivo."}