# GameStore API

> Backend modular para un e-commerce de videojuegos · Python 3.13 · FastAPI · SQLAlchemy · PostgreSQL (Supabase) · JWT · Passlib

---

## Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno (.env)](#configuración-del-entorno-env)
5. [Ejecutar el Servidor](#ejecutar-el-servidor)
6. [Automatización de Datos (Seeding)](#automatización-de-datos-seeding)
7. [Endpoints de la API](#endpoints-de-la-api)
8. [Seguridad y Autenticación](#seguridad-y-autenticación)
9. [Base de Datos](#base-de-datos)
10. [Quick Start](#quick-start)

---

## Descripción del Proyecto

**GameStore API** es un backend modular diseñado para gestionar una tienda de videojuegos online. Construido con **FastAPI** y siguiendo una arquitectura limpia por capas, esta versión avanzada proporciona:

- **Seguridad Robusta**: Hashing de contraseñas con Passlib (Bcrypt) y protección de rutas mediante Bearer Tokens (JWT).
- **Base de Datos en la Nube**: Migración a PostgreSQL gestionado en Supabase con conexión optimizada mediante Transaction Pooler.
- **Catálogo Real**: Integración con la RAWG API para importar títulos reales con imagen, género y plataforma.
- **Gestión de Carrito**: Sistema completo de persistencia para el carrito de compras ligado a usuarios autenticados.
- **Sistema de Pedidos**: Proceso de checkout que convierte el carrito en un pedido cerrado, registrando el precio histórico y restando stock.
- **Configuración Segura**: Manejo de claves y variables críticas mediante archivos de entorno.
- **Soporte Frontend**: Configuración de CORS lista para la integración con clientes modernos (Vite/React).

---

## Stack Tecnológico

| Tecnología       | Versión  | Propósito                                           |
|------------------|----------|-----------------------------------------------------|
| Python           | 3.13     | Lenguaje principal                                  |
| FastAPI          | Latest   | Framework web ASGI de alto rendimiento              |
| SQLAlchemy       | Latest   | ORM — modelos y abstracción de base de datos        |
| PostgreSQL       | Cloud    | Base de datos relacional en la nube (Supabase)      |
| psycopg2-binary  | Latest   | Driver de comunicación con PostgreSQL               |
| Passlib          | v1.7.4   | Gestión profesional de hashing (Bcrypt)             |
| PyJWT            | v2.8.0   | Generación y validación de tokens JWT               |
| python-dotenv    | Latest   | Carga de variables de entorno desde `.env`          |
| httpx            | Latest   | Cliente HTTP asíncrono para integración con APIs    |
| python-multipart | Latest   | Soporte de formularios para Login/OAuth2 en FastAPI |
| Uvicorn          | Latest   | Servidor ASGI con soporte hot-reload                |

---

## Estructura del Proyecto

```
TFG-DAW/
├── Models/
│   ├── game.py           # GameORM (incluye image_url) + esquemas Pydantic
│   ├── user.py           # UserORM + esquemas Pydantic
│   ├── cart.py           # CartORM y CartItemORM
│   └── order.py          # OrderORM y OrderItemORM
├── Routes/
│   ├── game_routes.py    # Endpoints /games (incluye importación RAWG)
│   ├── user_routes.py    # Endpoints /auth (Login/Register)
│   ├── cart_routes.py    # Endpoints /cart (Protegidos)
│   └── order_routes.py   # Endpoints /orders (Protegidos)
├── Services/
│   ├── game_service.py   # Lógica de catálogo e integración RAWG
│   ├── user_service.py   # Gestión de usuarios y hashing
│   ├── auth_service.py   # Validación JWT y dependencias
│   ├── cart_service.py   # Lógica del carrito de compra
│   └── order_service.py  # Lógica de checkout y pedidos
├── .env                  # Variables sensibles (No incluido en Git)
├── database.py           # Motor SQLAlchemy + get_db()
├── main.py               # Entrada principal + Middleware CORS
├── seed_from_api.py      # Script de carga masiva desde RAWG
└── requirements.txt      # Listado de dependencias del proyecto
```

### Responsabilidades por Capa

| Capa         | Responsabilidad                                                                       |
|--------------|---------------------------------------------------------------------------------------|
| **Models**   | Define las clases ORM (`UserORM`, `GameORM`, `OrderORM`...) y los esquemas Pydantic   |
| **Services** | Hashing de contraseñas, validaciones de negocio, gestión de stock y pedidos           |
| **Routes**   | Endpoints HTTP, mapeo a servicios e inyección de sesión de base de datos              |
| **database** | Configuración del motor SQLAlchemy y dependencia `get_db()`                           |

---

## Configuración del Entorno (.env)

Por seguridad, las claves de cifrado y credenciales no están hardcodeadas. Debes crear un archivo llamado `.env` en la raíz del proyecto con el siguiente formato:

```env
# --- Security ---
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# --- Database ---
# Usa URL Encoding en la contraseña si contiene caracteres especiales (ej: @ → %40)
DATABASE_URL=postgresql://usuario:contraseña@host:6543/postgres

# --- External APIs ---
RAWG_API_KEY=tu_clave_rawg_aqui
```

> **Nota sobre `DATABASE_URL`**: El proyecto se conecta a Supabase mediante el **Transaction Pooler** (puerto `6543`) en lugar del puerto estándar (`5432`). Esto evita problemas de resolución de nombres (DNS/IPv4/IPv6) y optimiza el rendimiento bajo conexiones concurrentes.

### 1. Crear el entorno virtual

```bash
python -m venv venv
```

### 2. Activar el entorno

**Windows:**
```bash
.\venv\Scripts\activate
```

**Unix / macOS:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar el Servidor

Desde la raíz del proyecto, ejecuta:

```bash
uvicorn main:app --reload
```

En el primer arranque, `main.py` ejecuta `Base.metadata.create_all()` y crea automáticamente todas las tablas necesarias en la base de datos de Supabase.

| URL                            | Descripción                          |
|--------------------------------|--------------------------------------|
| `http://127.0.0.1:8000`        | Raíz de la API                       |
| `http://127.0.0.1:8000/docs`   | Swagger UI — explorador interactivo  |
| `http://127.0.0.1:8000/redoc`  | ReDoc — documentación alternativa    |

---

## Automatización de Datos (Seeding)

El proyecto incluye el script `seed_from_api.py` para realizar una carga masiva inicial del catálogo con títulos reales.

**¿Qué hace el script?**
- Consulta la **RAWG API** y extrae los datos de 50 títulos reales (nombre, género, plataforma e imagen).
- Persiste los juegos directamente en Supabase.
- Gestiona duplicados automáticamente para evitar registros repetidos.
- Maneja errores de transacción con `db.rollback()` para garantizar la integridad de los datos.

**Ejecución:**
```bash
python seed_from_api.py
```

> Asegúrate de tener la variable `RAWG_API_KEY` definida en tu `.env` antes de ejecutar el script.

---

## Endpoints de la API

### Autenticación — `/auth`

| Método | Ruta             | Descripción                                       |
|--------|------------------|---------------------------------------------------|
| POST   | `/auth/register` | Registra un nuevo usuario con contraseña hasheada |
| POST   | `/auth/login`    | Valida credenciales y devuelve un token JWT       |

### Catálogo de Juegos — `/games`

| Método | Ruta                   | Descripción                                   |
|--------|------------------------|-----------------------------------------------|
| GET    | `/games/`              | Obtiene todos los juegos del catálogo         |
| GET    | `/games/{id}`          | Obtiene un juego por su ID                    |
| POST   | `/games/import/{name}` | Importa un juego desde la RAWG API por nombre |
| POST   | `/games/`              | Crea un nuevo juego manualmente               |
| PUT    | `/games/{id}`          | Actualiza un juego existente                  |
| DELETE | `/games/{id}`          | Elimina un juego del catálogo                 |

### Carrito de Compra — `/cart` *(Requiere token JWT)*

| Método | Ruta                | Descripción                                |
|--------|---------------------|--------------------------------------------|
| GET    | `/cart/`            | Obtiene el carrito del usuario autenticado |
| POST   | `/cart/add`         | Añade un juego al carrito                  |
| DELETE | `/cart/remove/{id}` | Elimina un juego del carrito               |
| DELETE | `/cart/clear`       | Vacía el carrito completamente             |

### Pedidos — `/orders` *(Requiere token JWT)*

| Método | Ruta               | Descripción                                                                        |
|--------|--------------------|------------------------------------------------------------------------------------|
| POST   | `/orders/checkout` | Convierte el carrito en un pedido cerrado, registra precio histórico y resta stock |
| GET    | `/orders/`         | Obtiene el historial de pedidos del usuario autenticado                            |

---

## Seguridad y Autenticación

### Hashing de Contraseñas

Se utiliza **Passlib** con el algoritmo **bcrypt** para transformar las contraseñas en hashes irreversibles. El texto plano nunca se persiste.

### Protección de Rutas (JWT)

El cliente se autentica en `/auth/login`. El servidor genera un token firmado con la `SECRET_KEY`. El cliente debe incluir este token en la cabecera de las peticiones protegidas:

```
Authorization: Bearer <TOKEN>
```

### Flujo de Registro

1. **Validación previa**: El servicio comprueba si el email o el username ya existen en la base de datos para evitar duplicados.
2. **Hashing**: La capa de servicio hashea la contraseña utilizando Passlib (con el motor bcrypt).
3. **Persistencia**: Se crea el nuevo registro en la tabla `users` almacenando únicamente el hash generado.
4. **Limpieza**: La contraseña en texto plano se descarta inmediatamente y nunca sale de la memoria volátil del servidor.

### Flujo de Login

1. **Identificación**: El cliente envía sus credenciales (email/password) en texto plano.
2. **Verificación**: El servicio recupera el hash del usuario y utiliza `pwd_context.verify()` para comparar la contraseña de forma segura (protegiendo el sistema contra timing attacks).
3. **Generación de Token**: Si las credenciales son válidas, el `auth_service` genera un JSON Web Token (JWT) firmado con la clave secreta del servidor.
4. **Respuesta**: El servidor devuelve un objeto con el `access_token` y el tipo de token (`bearer`), permitiendo al cliente acceder a las rutas protegidas.

---

## Base de Datos

El proyecto usa **PostgreSQL** en la nube a través de **Supabase**. La conexión se realiza mediante el **Transaction Pooler** (puerto `6543`) para optimizar las conexiones concurrentes y evitar problemas de resolución DNS.

### Esquema

**Tabla `users`**

| Columna           | Tipo    | Notas                         |
|-------------------|---------|-------------------------------|
| `id`              | INTEGER | Clave primaria, autoincrement |
| `username`        | VARCHAR | Único, no nulo                |
| `email`           | VARCHAR | Único, formato validado       |
| `hashed_password` | VARCHAR | Hash bcrypt                   |

**Tabla `games`**

| Columna       | Tipo    | Notas                                       |
|---------------|---------|---------------------------------------------|
| `id`          | INTEGER | Clave primaria, autoincrement               |
| `title`       | VARCHAR | Título del juego, no nulo                   |
| `price`       | FLOAT   | Precio unitario                             |
| `stock`       | INTEGER | Cantidad disponible                         |
| `description` | TEXT    | Descripción opcional                        |
| `image_url`   | VARCHAR | URL de portada (procedente de RAWG)         |

**Tabla `carts`**

| Columna   | Tipo    | Notas                          |
|-----------|---------|--------------------------------|
| `id`      | INTEGER | Clave primaria, autoincrement  |
| `user_id` | INTEGER | Clave foránea → `users.id`     |

**Tabla `cart_items`**

| Columna    | Tipo    | Notas                          |
|------------|---------|--------------------------------|
| `id`       | INTEGER | Clave primaria, autoincrement  |
| `cart_id`  | INTEGER | Clave foránea → `carts.id`     |
| `game_id`  | INTEGER | Clave foránea → `games.id`     |
| `quantity` | INTEGER | Cantidad de unidades           |

**Tabla `orders`**

| Columna      | Tipo     | Notas                          |
|--------------|----------|--------------------------------|
| `id`         | INTEGER  | Clave primaria, autoincrement  |
| `user_id`    | INTEGER  | Clave foránea → `users.id`     |
| `created_at` | DATETIME | Fecha y hora del pedido        |

**Tabla `order_items`**

| Columna          | Tipo    | Notas                                        |
|------------------|---------|----------------------------------------------|
| `id`             | INTEGER | Clave primaria, autoincrement                |
| `order_id`       | INTEGER | Clave foránea → `orders.id`                  |
| `game_id`        | INTEGER | Clave foránea → `games.id`                   |
| `quantity`       | INTEGER | Cantidad comprada                            |
| `price_at_order` | FLOAT   | Precio histórico en el momento de la compra  |

---

## Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/ErPinguino/TFG-DAW.git
cd TFG-DAW

# 2. Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Unix/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar las variables de entorno
# Crear el archivo .env con SECRET_KEY, DATABASE_URL y RAWG_API_KEY

# 5. (Opcional) Poblar el catálogo con 50 juegos reales desde RAWG
python seed_from_api.py

# 6. Arrancar el servidor
uvicorn main:app --reload

# 7. Abrir la documentación interactiva
# http://127.0.0.1:8000/docs
```

---

*GameStore API — TFG-DAW*
