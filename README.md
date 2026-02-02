# 🤟 Sign Technology

## Sistema de Traducción de Lenguaje de Señas Colombiano (LSC)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![License](https://img.shields.io/badge/License-ISC-blue?style=for-the-badge)](LICENSE)

Plataforma integral para la traducción bidireccional de Lenguaje de Señas Colombiano utilizando inteligencia artificial

[📖 Documentación](#-documentación-de-la-api) • [🚀 Inicio Rápido](#-inicio-rápido) • [🏗️ Arquitectura](#️-arquitectura-del-proyecto) • [🤝 Contribuir](#-contribuidores)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Inicio Rápido](#-inicio-rápido)
- [Configuración](#️-configuración)
- [Documentación de la API](#-documentación-de-la-api)
- [Base de Datos](#️-base-de-datos)
- [Tecnologías](#️-tecnologías-utilizadas)
- [Seguridad](#-seguridad)
- [Licencia](#-licencia)

---

## ✨ Características

| Característica | Descripción |
| -------------- | ----------- |
| 🔄 **Traducción Bidireccional** | Conversión de texto a señas y señas a texto |
| 🤖 **Inteligencia Artificial** | Modelo de IA para reconocimiento y traducción |
| 👥 **Gestión de Usuarios** | Sistema completo de roles (Admin/Colaborador) |
| 📊 **Dashboard Analítico** | Estadísticas y métricas en tiempo real |
| 🤝 **Contribuciones** | Sistema colaborativo para aportar nuevas señas |
| 📝 **Reportes** | Gestión de errores y mejoras del sistema |
| 🔐 **Autenticación JWT** | Sistema seguro de autenticación con tokens |
| 📱 **Diseño Responsivo** | Interfaz adaptable a cualquier dispositivo |

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura de **microservicios** con separación clara entre backend y frontend:

```text
PROYECTO-SENA/
│
├── 📁 fastapi/                    # 🔷 Backend - API REST (FastAPI)
│   ├── 📁 app/
│   │   ├── 📁 api/v1/             # Versionado de API
│   │   │   ├── 📁 endpoints/      # Controladores de rutas
│   │   │   │   ├── auth.py        # Autenticación
│   │   │   │   ├── usuarios.py    # Gestión de usuarios
│   │   │   │   ├── contribuciones.py
│   │   │   │   ├── reportes.py
│   │   │   │   └── estadisticas.py
│   │   │   └── router.py          # Router principal
│   │   ├── 📁 core/               # Configuración central
│   │   │   ├── config.py          # Variables de entorno
│   │   │   ├── database.py        # Conexión MySQL
│   │   │   └── security.py        # JWT y seguridad
│   │   ├── 📁 schemas/            # Esquemas Pydantic
│   │   ├── 📁 services/           # Lógica de negocio
│   │   └── main.py                # Punto de entrada
│   └── requirements.txt
│
├── 📁 frontend/                   # 🟢 Frontend - Servidor Web (Flask)
│   ├── 📁 static/
│   │   ├── 📁 css/                # Estilos organizados
│   │   │   ├── 📁 components/     # Estilos de componentes
│   │   │   └── 📁 pages/          # Estilos por página
│   │   ├── 📁 js/                 # JavaScript modular
│   │   ├── 📁 img/                # Recursos gráficos
│   │   └── 📁 video/              # Videos de señas
│   ├── 📁 templates/
│   │   ├── 📁 components/         # Componentes reutilizables
│   │   ├── 📁 pages/              # Páginas de la aplicación
│   │   ├── base.html              # Template base
│   │   └── base_admin.html        # Template administración
│   ├── run.py                     # Servidor Flask
│   └── requirements.txt
│
├── 📁 db/                         # 🗄️ Base de Datos
│   └── sign_technology.sql        # Script de creación
│
└── README.md
```

---

## 📦 Requisitos Previos

Asegúrate de tener instalado:

| Requisito | Versión Mínima | Verificar Instalación |
| --------- | -------------- | --------------------- |
| Python | 3.10+ | `python --version` |
| MySQL | 8.0+ | `mysql --version` |
| Git | 2.0+ | `git --version` |

---

## 🚀 Inicio Rápido

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/sign-technology.git
cd sign-technology
```

### 2️⃣ Configurar Base de Datos

```bash
# Conectar a MySQL e importar el esquema
mysql -u root -p < db/sign_technology.sql
```

### 3️⃣ Configurar Backend (FastAPI)

```bash
# Navegar al directorio del backend
cd fastapi

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (ver sección de configuración)

# Ejecutar servidor de desarrollo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4️⃣ Configurar Frontend (Flask)

```bash
# En otra terminal, navegar al frontend
cd frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python run.py
```

### 5️⃣ Acceder a la Aplicación

| Servicio | URL | Descripción |
| -------- | --- | ----------- |
| 🌐 Frontend | <http://localhost:5000> | Interfaz de usuario |
| 🔷 API | <http://localhost:8000> | Backend REST |
| 📚 Swagger UI | <http://localhost:8000/docs> | Documentación interactiva |
| 📖 ReDoc | <http://localhost:8000/redoc> | Documentación alternativa |

---

## ⚙️ Configuración

### Variables de Entorno (.env)

Crear archivo `.env` en el directorio `fastapi/`:

```env
# ═══════════════════════════════════════════════════════════
# 🗄️ BASE DE DATOS
# ═══════════════════════════════════════════════════════════
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_seguro
DB_NAME=sign_technology

# ═══════════════════════════════════════════════════════════
# 🔐 SEGURIDAD JWT
# ═══════════════════════════════════════════════════════════
SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

# ═══════════════════════════════════════════════════════════
# 🌐 CORS
# ═══════════════════════════════════════════════════════════
CORS_ORIGINS=http://localhost:5000,http://localhost:3000
```

> ⚠️ **Importante:** Nunca subas el archivo `.env` al repositorio. Asegúrate de incluirlo en `.gitignore`.

---

## 📖 Documentación de la API

### Prefijo Base: `/api/v1`

### 🔐 Autenticación

| Método | Endpoint | Descripción |
| ------ | ------------ | ----------- |
| `POST` | `/auth/login` | Iniciar sesión |

### 📊 Estadísticas

| Método | Endpoint | Descripción |
| ------ | --------------- | ---------------------------- |
| `GET` | `/estadisticas` | Obtener métricas del sistema |

### 👥 Usuarios

| Método | Endpoint | Descripción |
| -------- | ------------------ | ------------------ |
| `GET` | `/usuarios` | Listar usuarios |
| `POST` | `/usuarios` | Crear usuario |
| `GET` | `/usuarios/{id}` | Obtener usuario |
| `PUT` | `/usuarios/{id}` | Actualizar usuario |
| `DELETE` | `/usuarios/{id}` | Eliminar usuario |

### 🤝 Contribuciones

| Método | Endpoint | Descripción |
| -------- | ------------------------ | ----------------------- |
| `GET` | `/contribuciones` | Listar contribuciones |
| `POST` | `/contribuciones` | Crear contribución |
| `PUT` | `/contribuciones/{id}` | Gestionar contribución |

### 📝 Reportes

| Método | Endpoint | Descripción |
| -------- | -------------------- | ------------------- |
| `GET` | `/reportes` | Listar reportes |
| `POST` | `/reportes` | Crear reporte |
| `PUT` | `/reportes/{id}` | Actualizar reporte |

> 📚 **Documentación Completa:** Accede a `/docs` o `/redoc` cuando el servidor esté en ejecución.

---

## 🗄️ Base de Datos

### Diagrama de Entidades Principales

```text
┌──────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│    roles     │────<│      usuarios        │────<│  contribuciones_senas   │
└──────────────┘     └──────────────────────┘     └─────────────────────────┘
                              │                              │
                              │                              ▼
                              │                  ┌─────────────────────────┐
                              │                  │ repositorio_senas_oficial│
                              │                  └─────────────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   traducciones   │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ reportes_errores │
                     └──────────────────┘
```

### Tablas Principales

| Tabla | Descripción |
| ----- | ----------- |
| `roles` | Roles del sistema (Administrador, Colaborador) |
| `usuarios` | Usuarios registrados |
| `usuarios_anonimos` | Visitantes no registrados |
| `contribuciones_senas` | Aportes de la comunidad |
| `repositorio_senas_oficial` | Señas validadas y aprobadas |
| `traducciones` | Historial de traducciones |
| `reportes_errores` | Reportes de fallos |
| `rendimiento_modelo` | Métricas del modelo IA |
| `tokens_recuperacion` | Tokens para recuperar contraseña |

### Vistas

- `vista_estadisticas` - Resumen estadístico del sistema

### Eventos Automáticos

- `ev_desactivar_usuarios_inactivos` - Inactiva colaboradores tras 1 año
- `ev_limpieza_tokens_expirados` - Limpia tokens expirados cada hora

---

## 🛠️ Tecnologías Utilizadas

### Backend

| Tecnología | Versión | Propósito |
| ---------- | ------- | -------------------- |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | 0.104.1 | Framework API REST |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat&logo=uvicorn&logoColor=white) | 0.24.0 | Servidor ASGI |
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white) | 2.5.2 | Validación de datos |
| ![PyMySQL](https://img.shields.io/badge/PyMySQL-4479A1?style=flat&logo=mysql&logoColor=white) | 1.1.0 | Conector MySQL |
| ![JWT](https://img.shields.io/badge/JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white) | - | Autenticación |
| ![bcrypt](https://img.shields.io/badge/bcrypt-003B57?style=flat&logoColor=white) | 4.0.1 | Hash de contraseñas |

### Frontend

| Tecnología | Versión | Propósito |
| ---------- | ------- | --------------------- |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | 3.0.0 | Servidor de templates |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | 5 | Estructura |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | 3 | Estilos |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | ES6+ | Lógica frontend |
| ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat&logo=jinja&logoColor=white) | - | Motor de templates |

### Base de Datos

| Tecnología | Versión | Propósito |
| ---------- | ------- | --------------- |
| ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) | 8.0+ | RDBMS principal |

---

## 🔒 Seguridad

### Medidas Implementadas

| Medida | Implementación |
| ------ | ------------------------------ |
| 🔐 **Hashing de Contraseñas** | bcrypt con salt automático |
| 🎫 **Autenticación** | JWT con expiración configurable |
| 🛡️ **Autorización** | Validación de roles por endpoint |
| 🌐 **CORS** | Configuración estricta de orígenes |
| 🔒 **SQL Injection** | Queries parametrizadas |
| ✅ **Validación** | Schemas Pydantic estrictos |

### Buenas Prácticas

```python
# ✅ Ejemplo de autenticación segura
Authorization: Bearer <token>
```

> 🔴 **Producción:** Recuerda cambiar `SECRET_KEY`, configurar HTTPS y restringir CORS.

---

## 🤝 Contribuidores

### Sign Technology Team

Desarrollado con ❤️ para la comunidad sorda colombiana

---

## 📄 Licencia

Este proyecto está bajo la Licencia **ISC**.

```text
ISC License

Copyright (c) 2026 Sign Technology Team

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
```

---

**[⬆ Volver arriba](#-sign-technology)**
