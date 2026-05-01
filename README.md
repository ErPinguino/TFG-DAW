# GameStore API

> Backend modular para un e-commerce de videojuegos · Python 3.14 · FastAPI · SQLAlchemy · SQLite · JWT · Passlib

---

## Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno (.env)](#configuración-del-entorno-env)
5. [Ejecutar el Servidor](#ejecutar-el-servidor)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Seguridad y Autenticación](#seguridad-y-autenticación)
8. [Base de Datos](#base-de-datos)
9. [Quick Start](#quick-start)

---

## Descripción del Proyecto

**GameStore API** es un backend modular diseñado para gestionar una tienda de videojuegos online. Construido con **FastAPI** y siguiendo una arquitectura limpia por capas, esta versión avanzada proporciona:

- **Seguridad Robusta**: Hashing de contraseñas con Passlib (Bcrypt) y protección de rutas mediante Bearer Tokens (JWT).
- **Gestión de Carrito**: Sistema completo de persistencia para el carrito de compras ligado a usuarios autenticados.
- **Configuración Segura**: Manejo de claves y variables críticas mediante archivos de entorno.
- **Soporte Frontend**: Configuración de CORS lista para la integración con clientes modernos (Vite/React).

---

## Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|----------|----------------------------------------------|
| Python | 3.14 | Lenguaje principal |
| FastAPI | Latest | Framework web ASGI de alto rendimiento |
| SQLAlchemy | Latest | ORM — modelos y abstracción de base de datos |
| SQLite | Built-in | Base de datos relacional local (archivo) |
| Passlib | v1.7.4 | Gestión profesional de hashing (Bcrypt) |
| PyJWT | v2.8.0 | Generación y validación de tokens JWT |
| python-dotenv | Latest | Carga de variables de entorno desde `.env` |
| Uvicorn | Latest | Servidor ASGI con soporte hot-reload |

---

## Estructura del Proyecto
```
TFG-DAW/
├── Models/
│   ├── game.py          # GameORM + esquemas Pydantic
│   ├── user.py          # UserORM + esquemas Pydantic
│   └── cart.py          # CartORM y CartItemORM
├── Routes/
│   ├── game_routes.py   # Endpoints /games
│   ├── user_routes.py   # Endpoints /auth (Login/Register)
│   └── cart_routes.py   # Endpoints /cart (Protegidos)
├── Services/
│   ├── game_service.py  # Lógica de catálogo
│   ├── user_service.py  # Gestión de usuarios y hashing
│   ├── auth_service.py  # Validación JWT y dependencias
│   └── cart_service.py  # Lógica del carrito de compra
├── .env                 # Variables sensibles (No incluido en Git)
├── database.py          # Motor SQLAlchemy + get_db()
├── main.py              # Entrada principal + Middleware CORS
├── requirements.txt     # Listado de dependencias del proyecto
└── gamestore.db         # SQLite (generado automáticamente)
```

### Responsabilidades por Capa

| Capa         | Responsabilidad                                                           |
|--------------|---------------------------------------------------------------------------|
| **Models**   | Define las clases ORM (`UserORM`, `GameORM`) y los esquemas Pydantic      |
| **Services** | Hashing de contraseñas, validaciones de negocio, gestión de stock         |
| **Routes**   | Endpoints HTTP, mapeo a servicios e inyección de sesión de base de datos  |
| **database** | Configuración del motor SQLAlchemy y dependencia `get_db()`               |

---

## Configuración del Entorno


Por seguridad, las claves de cifrado no están hardcodeadas. Debes crear un archivo llamado `.env` en la raíz del proyecto con el siguiente formato:
```env
SECRET_KEY=tu_clave_secreta_super_aleatoria_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

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

En el primer arranque, `main.py` ejecuta `Base.metadata.create_all()` y crea automáticamente el archivo `gamestore.db` con todas las tablas necesarias.

| URL                            | Descripción                          |
|--------------------------------|--------------------------------------|
| `http://127.0.0.1:8000`        | Raíz de la API                       |
| `http://127.0.0.1:8000/docs`   | Swagger UI — explorador interactivo  |
| `http://127.0.0.1:8000/redoc`  | ReDoc — documentación alternativa    |

---

## Endpoints de la API

### Autenticación — `/auth`

| Método | Ruta             | Descripción                                      |
|--------|------------------|--------------------------------------------------|
| POST   | `/auth/register` | Registra un nuevo usuario con contraseña hasheada |
| POST   | `/auth/login`    | Valida credenciales y autentica al usuario        |

### Catálogo de Juegos — `/games`

| Método | Ruta          | Descripción                          |
|--------|---------------|--------------------------------------|
| GET    | `/games/`     | Obtiene todos los juegos del catálogo |
| GET    | `/games/{id}` | Obtiene un juego por su ID           |
| POST   | `/games/`     | Crea un nuevo juego                  |
| PUT    | `/games/{id}` | Actualiza un juego existente         |
| DELETE | `/games/{id}` | Elimina un juego del catálogo        |

### Carrito de compra — `/cart` (Requiere token)
| Método | Ruta          | Descripción                          |
|--------|---------------|--------------------------------------|
| GET    | `/cart/`      | Obtiene el carrito del usuario autenticado |
| POST   | `/cart/add`   | Añade un juego al carrito            |
| DELETE | `/cart/remove/{id}` | Elimina un juego del carrito   |
| DELETE | `/cart/clear` | Vacía el carrito                     |




---

## Seguridad

Hashing de Contraseñas
Se utiliza passlib con el algoritmo bcrypt para transformar las contraseñas en hashes irreversibles. El texto plano nunca se persiste.

Protección de Rutas (JWT)
El cliente se autentica en /auth/login.

El servidor genera un token firmado con la SECRET_KEY.

El cliente debe incluir este token en la cabecera de las peticiones protegidas:
Authorization: Bearer <TOKEN>

### Flujo de Registro

Validación Previa: El servicio comprueba si el email o el username ya existen en la base de datos para evitar duplicados.

Hashing: La capa de servicio hashea la contraseña utilizando passlib (con el motor bcrypt).

Persistencia: Se crea el nuevo registro en la tabla users almacenando únicamente el hash generado.

Limpieza: La contraseña en texto plano se descarta inmediatamente y nunca sale de la memoria volátil del servidor.

### Flujo de Login

dentificación: El cliente envía sus credenciales (email/password) en texto plano.

Verificación: El servicio recupera el hash del usuario y utiliza pwd_context.verify() para comparar la contraseña de forma segura (protegiendo el sistema contra timing attacks).

Generación de Token: Si las credenciales son válidas, el auth_service genera un JSON Web Token (JWT) firmado con la clave secreta del servidor.

Respuesta: El servidor devuelve un objeto con el access_token y el tipo de token (bearer), permitiendo al cliente acceder a las rutas protegidas (como el carrito).

---

## Base de Datos

El proyecto usa **SQLite** como base de datos local sin configuración adicional. El archivo `gamestore.db` se crea automáticamente mediante SQLAlchemy al arrancar la aplicación.

### Esquema

**Tabla `users`**

| Columna             | Tipo    | Notas                      |
|---------------------|---------|----------------------------|
| `id`                | INTEGER | Clave primaria, autoincrement |
| `username`          | VARCHAR | Único, no nulo             |
| `email`             | VARCHAR | Único, formato validado    |
| `hashed_password`   | VARCHAR | Hash bcrypt                |

**Tabla `games`**

| Columna       | Tipo    | Notas                         |
|---------------|---------|-------------------------------|
| `id`          | INTEGER | Clave primaria, autoincrement |
| `title`       | VARCHAR | Título del juego, no nulo     |
| `price`       | FLOAT   | Precio unitario               |
| `stock`       | INTEGER | Cantidad disponible           |
| `description` | TEXT    | Descripción opcional          |

**Tabla `carts`**

| Columna       | Tipo    | Notas                         |
|---------------|---------|-------------------------------|
| `id`          | INTEGER | Clave primaria, autoincrement |
| `user_id`     | INTEGER | Clave foránea, a quien pertenece |

**Tabla `cart_items`**

| Columna       | Tipo    | Notas                         |
|---------------|---------|-------------------------------|
| `id`          | INTEGER | Clave primaria, autoincrement |
| `cart_id`     | INTEGER | Clave foránea, a qué carrito pertenece |
| `game_id`     | INTEGER | Clave foránea, qué juego es   |
| `quantity`    | INTEGER | Cantidad   |



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

# 4. Arrancar el servidor
uvicorn main:app --reload

# 5. Abrir la documentación interactiva
# http://127.0.0.1:8000/docs
```

---

*GameStore API — TFG-DAW*