# Documentación Técnica - API SignTechnology

## Descripción General

API REST desarrollada con FastAPI para la gestión del sistema SignTechnology. Implementa autenticación JWT, pool de conexiones a MySQL y arquitectura modular por capas.

## Arquitectura por Capas

### Principio de Dependencias

**Regla fundamental:** Las capas superiores pueden llamar a las inferiores, pero las inferiores NUNCA conocen a las superiores.

```text
Capa 5: Main (Aplicación)
    ↓
Capa 4: API (Endpoints)
    ↓
Capa 3: Services (Lógica de Negocio)
    ↓
Capa 2: Schemas (Validación)
    ↓
Capa 1: Core (Infraestructura)
```

### Orden Lógico de Capas (de base a tope)

#### Capa 1: Infraestructura (Core)

**Ubicación:** `app/core/`
**Responsabilidad:** Configuración, base de datos, seguridad
**No depende de:** Ninguna otra capa del proyecto

```python
core/
├── config.py       # Variables de entorno y configuración
├── database.py     # Pool de conexiones a MySQL
└── security.py     # JWT, bcrypt, autenticación
```

**Reglas:**

- NO debe importar de `api`, `services` o `schemas`
- Solo utilidades y librerías externas
- Es la base de todo

#### Capa 2: Validación (Schemas)

**Ubicación:** `app/schemas/`
**Responsabilidad:** Contratos de datos, validación con Pydantic
**Depende de:** Ninguna (solo Pydantic)

```python
schemas/
├── auth.py            # Modelos de autenticación
├── usuarios.py        # Modelos de usuarios
├── contribuciones.py  # Modelos de contribuciones
└── ...
```

**Reglas:**

- Define estructura de request/response
- NO debe importar de `api`, `services` o `core`
- Solo Pydantic y tipos Python

#### Capa 3: Negocio (Services)

**Ubicación:** `app/services/`
**Responsabilidad:** Lógica de negocio, reglas, procesos
**Depende de:** Capa 1 (core) y Capa 2 (schemas)

```python
services/
├── auth.py            # Lógica de autenticación
├── usuarios.py        # Lógica de gestión de usuarios
├── contribuciones.py  # Lógica de contribuciones
└── ...
```

**Reglas:**

- Contiene toda la lógica de negocio
- Usa `get_connection()` de `core.database`
- Retorna datos, NO objetos HTTP
- NO debe importar de `api`

**Ejemplo correcto:**

```python
from app.core.database import get_connection
from app.core.security import hash_password

def crear_usuario(usuario: UsuarioCreate):
    conn = get_connection()
    # ... lógica
    return user_id
```

**Ejemplo INCORRECTO:**

```python
from fastapi import HTTPException  # ❌ NO en services
```

#### Capa 4: Presentación (API/Endpoints)

**Ubicación:** `app/api/v1/endpoints/`
**Responsabilidad:** Recibir peticiones HTTP, validar, delegar a services
**Depende de:** Capa 3 (services), Capa 2 (schemas)

```python
api/v1/endpoints/
├── auth.py            # Endpoints de autenticación
├── usuarios.py        # Endpoints de usuarios
├── contribuciones.py  # Endpoints de contribuciones
└── ...
```

**Reglas:**

- Solo maneja HTTP (request/response)
- Valida datos con schemas
- Delega lógica a services
- Maneja excepciones HTTP

**Ejemplo correcto:**

```python
@router.post("/usuarios/")
def create_user(usuario: UsuarioCreate):
    user_id = user_service.crear_usuario(usuario)  # ✅ Delega a service
    return {"id": user_id}
```

#### Capa 5: Aplicación (Main)

**Ubicación:** `app/main.py`
**Responsabilidad:** Configurar app, middlewares, lifecycle
**Depende de:** Todas las capas anteriores

```python
main.py  # Punto de entrada, orquestación
```

### Flujo de una Petición

```text
1. HTTP Request → Endpoint (api/endpoints)
2. Endpoint valida con Schema
3. Endpoint llama a Service
4. Service ejecuta lógica de negocio
5. Service usa Core (DB, seguridad)
6. Service retorna datos
7. Endpoint transforma a HTTP Response
```

### Errores Comunes a Evitar

❌ **Core importando API**

```python
# En core/database.py
from app.api.v1.endpoints import usuarios  # ❌ NUNCA
```

❌ **Services usando objetos HTTP**

```python
# En services/usuarios.py
from fastapi import Request  # ❌ NO
def mi_funcion(request: Request):  # ❌ NO
```

❌ **Endpoints con SQL directo**

```python
# En api/endpoints/usuarios.py
cursor.execute("SELECT * FROM usuarios")  # ❌ NO
# Debe estar en services
```

❌ **Services importando endpoints**

```python
# En services/auth.py
from app.api.v1.endpoints.auth import login  # ❌ NUNCA
```

### Verificación Rápida

Si tu código cumple esto, las capas están bien:

✅ `core` no importa nada del proyecto
✅ `schemas` no importa nada del proyecto
✅ `services` solo importa `core` y `schemas`
✅ `api` importa `services` y `schemas`
✅ `main.py` importa todo

## Arquitectura del Proyecto

```text
api/
├── app/
│   ├── main.py                     # Punto de entrada de la aplicación
│   ├── core/                       # Configuración central
│   │   ├── config.py              # Variables de entorno
│   │   ├── database.py            # Pool de conexiones MySQL
│   │   └── security.py            # JWT y encriptación bcrypt
│   ├── api/v1/                    # Endpoints de la API
│   │   ├── router.py              # Router principal
│   │   └── endpoints/             # Módulos de endpoints
│   ├── services/                  # Lógica de negocio
│   └── schemas/                   # Modelos de validación Pydantic
├── .env                           # Variables de entorno (no versionar)
└── requirements.txt               # Dependencias
```

## Configuración

### Variables de Entorno (.env)

```env
# Base de Datos
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sign_technology

# Pool de Conexiones
DB_POOL_SIZE=20              # Conexiones activas
DB_MAX_OVERFLOW=10           # Conexiones adicionales
DB_POOL_RECYCLE=3600        # Segundos antes de reciclar
DB_POOL_PRE_PING=True       # Verificar antes de usar

# JWT
SECRET_KEY=clave_secreta_compleja
ACCESS_TOKEN_EXPIRE=30      # Minutos
ALGORITHM=HS256

# CORS
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
```

## Pool de Conexiones

El sistema utiliza DBUtils para mantener un pool de conexiones reutilizables:

- **Capacidad**: 20 conexiones activas + 10 overflow = 30 total
- **Ventajas**: Reduce latencia, mejora rendimiento en peticiones concurrentes
- **Gestión**: Inicialización automática al arrancar, cierre al detener

### Uso en Servicios

```python
from app.core.database import get_connection

def mi_funcion():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tabla")
            return cursor.fetchall()
    finally:
        conn.close()  # Importante: devolver al pool
```

## Seguridad

### Encriptación de Contraseñas (bcrypt)

```python
from app.core.security import hash_password, verify_password

# Al registrar usuario
hashed = hash_password("password123")

# Al validar login
is_valid = verify_password("password123", hashed)
```

### Tokens JWT

```python
from app.core.security import create_access_token, decode_token

# Generar token
token = create_access_token({"user_id": 1, "token": "user@mail.com"})

# Validar token
payload = decode_token(token)
```

## Endpoints Principales

### Autenticación

**POST** `/api/v1/auth/login`

Request:

```json
{
  "correo": "usuario@mail.com",
  "contrasena": "password"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id_usuario": 1,
    "nombre_completo": "Juan Pérez",
    "correo": "usuario@mail.com",
    "id_rol": 1,
    "nombre_rol": "Administrador"
  }
}
```

### Usuarios

- **GET** `/api/v1/usuarios/` - Listar usuarios (con paginación y filtros)
- **POST** `/api/v1/usuarios/` - Crear usuario
- **GET** `/api/v1/usuarios/{id}` - Obtener usuario específico
- **PUT** `/api/v1/usuarios/{id}` - Actualizar usuario
- **DELETE** `/api/v1/usuarios/{id}` - Eliminar usuario
- **GET** `/api/v1/usuarios/stats` - Estadísticas de usuarios

## Ejecución

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar .env

Copiar y ajustar las variables de entorno según el entorno.

### Ejecutar servidor

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Documentación interactiva

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Buenas Prácticas

1. **Conexiones**: Siempre cerrar conexiones en bloque `finally`
2. **Validación**: Usar schemas de Pydantic para validar datos
3. **Errores**: Capturar excepciones y devolver mensajes descriptivos
4. **Seguridad**: Nunca exponer contraseñas, ni siquiera hashes
5. **Logs**: Registrar errores relevantes en consola

## Notas Técnicas

- **Autocommit**: Habilitado en el pool, no requiere commits manuales
- **Charset**: utf8mb4 para soporte completo de caracteres
- **Cursores**: DictCursor para resultados como diccionarios
- **Timeouts**: Pool usa blocking=True, espera si no hay conexiones

---

## Proyecto SENA - SignTechnology 2026
