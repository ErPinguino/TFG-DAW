from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Models import cart, game, order, user

from Routes import (
    cart_routes,
    game_routes,
    order_routes,
    user_routes
)

from database import engine, Base

# =========================
# APP
# =========================

app = FastAPI(

    title="GameStore API",

    description="Backend del e-commerce de videojuegos",

    version="1.0.0"

)

# =========================
# CORS
# =========================

origins = [

    # Vite
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # Live Server VSCode
    "http://127.0.0.1:5500",
    "http://localhost:5500",

    # React
    "http://localhost:3000",

]

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# =========================
# BASE DE DATOS
# =========================

Base.metadata.create_all(bind=engine)

# =========================
# ROUTERS
# =========================

app.include_router(game_routes.router)

app.include_router(user_routes.router)

app.include_router(cart_routes.router)

app.include_router(order_routes.router)

# =========================
# ROOT
# =========================

@app.get("/")
def read_root():

    return {

        "mensaje": "¡Bienvenido a GameStore! El servidor está funcionando correctamente."

    }