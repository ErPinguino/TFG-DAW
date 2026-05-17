import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database import Base, get_db
from Models.user import UserORM
from Models.game import GameORM
from Models.order import OrderORM, OrderItemORM
try:
    from Models.cart import CartItemORM 
except ImportError:
    pass

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

token_usuario = ""



def test_register_user_success():
    """1. Registro de usuario base"""
    response = client.post(
        "/auth/register",
        json={
            "username": "comprador",
            "email": "comprador@example.com",
            "password": "password123"
        }
    )
    assert response.status_code in [200, 201]


def test_login_user_success():
    global token_usuario
    response = client.post(
        "/auth/login", 
        data={
            "username": "comprador",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token_usuario = data["access_token"] 


def test_get_catalog_public():
    """3. Test estático del catálogo público"""
    response = client.get("/games/?page=1&size=5")
    assert response.status_code == 200


def test_cart_and_checkout_flow():
    """4. EL TEST FINAL: Cesta, compra e historial de pedidos"""
    global token_usuario
    headers = {"Authorization": f"Bearer {token_usuario}"}

    db = TestingSessionLocal()
    juego_test = GameORM(
        title="Elden Ring Test",
        genre="RPG",
        platform="PC",
        price=60.0,
        stock=5,
        image_url="http://example.com/elden.jpg",
        is_active=True
    )
    db.add(juego_test)
    db.commit()
    db.refresh(juego_test)
    db.close()

    response_add_cart = client.post(
        "/cart/add",
        json={"game_id": juego_test.id, "quantity": 1},
        headers=headers
    )
    assert response_add_cart.status_code in [200, 201]

    response_get_cart = client.get("/cart/", headers=headers)
    assert response_get_cart.status_code == 200

    response_checkout = client.post("/orders/checkout", headers=headers)
    assert response_checkout.status_code in [200, 201]

    response_history = client.get("/orders/me", headers=headers)
    assert response_history.status_code == 200
    orders = response_history.json()
    
    assert len(orders) > 0
    assert orders[0]["total_price"] == 60.0
    assert orders[0]["status"] == "completed"