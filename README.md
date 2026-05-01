# GameStore API

> Backend modular para un e-commerce de videojuegos · Python 3.14 · FastAPI · SQLAlchemy · SQLite · Bcrypt

---

## Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Ejecutar el Servidor](#ejecutar-el-servidor)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Seguridad](#seguridad)
8. [Base de Datos](#base-de-datos)
9. [Quick Start](#quick-start)

---

## Descripción del Proyecto

**GameStore API** es un backend modular diseñado para gestionar una tienda de videojuegos online. Construido con **FastAPI** y siguiendo una arquitectura limpia por capas, proporciona:

- Autenticación segura de usuarios con hashing de contraseñas
- Gestión completa del catálogo de juegos (CRUD)
- Persistencia con SQLite, generada automáticamente en el primer arranque
- Documentación interactiva integrada (Swagger UI)

---

## Stack Tecnológico

| Tecnología | Versión  | Propósito                                    |
|------------|----------|----------------------------------------------|
| Python     | 3.14     | Lenguaje principal                           |
| FastAPI    | Latest   | Framework web ASGI de alto rendimiento       |
| SQLAlchemy | Latest   | ORM — modelos y abstracción de base de datos |
| SQLite     | Built-in | Base de datos relacional local (archivo)     |
| Bcrypt     | Latest   | Hashing seguro de contraseñas                |
| Pydantic   | v2       | Validación de esquemas y serialización       |
| Uvicorn    | Latest   | Servidor ASGI con soporte hot-reload         |

---

## Estructura del Proyecto

```
TFG-DAW/
├── Models/
│   ├── __init__.py
│   ├── game.py          # GameORM + esquemas Pydantic
│   └── user.py          # UserORM + esquemas Pydantic
├── Routes/
│   ├── __init__.py
│   ├── game_routes.py   # Endpoints /games
│   └── user_routes.py   # Endpoints /auth
├── Services/
│   ├── __init__.py
│   ├── game_service.py  # Lógica de negocio de juegos
│   └── user_service.py  # Lógica de autenticación
├── database.py          # Motor SQLAlchemy + get_db()
├── main.py              # Entrada principal + inicialización DB
├── gamestore.db         # SQLite (generado automáticamente)
└── venv/                # Entorno virtual
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
pip install fastapi uvicorn[standard] sqlalchemy pydantic email-validator bcrypt
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

---

## Seguridad

Las contraseñas se gestionan exclusivamente como hashes bcrypt. El texto plano nunca se almacena ni se registra en logs.

### Flujo de Registro

1. El cliente envía username, email y contraseña en texto plano
2. La capa de servicio hashea la contraseña con `bcrypt`
3. Solo el hash se persiste en la tabla `users`
4. La contraseña original se descarta inmediatamente

### Flujo de Login

1. El cliente envía username y contraseña en texto plano
2. El servicio recupera el hash almacenado para ese usuario
3. `bcrypt.checkpw()` compara el texto plano contra el hash (resistente a timing attacks)
4. La autenticación se acepta o rechaza — sin implementación de token en la versión actual

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
pip install fastapi uvicorn[standard] sqlalchemy pydantic email-validator bcrypt

# 4. Arrancar el servidor
uvicorn main:app --reload

# 5. Abrir la documentación interactiva
# http://127.0.0.1:8000/docs
```

---

*GameStore API — TFG-DAW*