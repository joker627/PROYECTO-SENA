# Sign Technology - Sistema de Traducción de Lenguaje de Señas LSC

Sistema completo para la traducción de Lenguaje de Señas Colombiano (LSC) utilizando inteligencia artificial.

## 📁 Estructura del Proyecto

```
PROYECTO/
├── api/                    # Backend Flask (API REST)
│   ├── config/            # Configuración (DB, conexiones)
│   ├── controllers/       # Controladores de rutas
│   ├── models/           # Modelos de datos
│   ├── middlewares/      # Middlewares (auth, etc.)
│   ├── utils/            # Utilidades (JWT, email, password)
│   └── app_api.py        # Aplicación principal Flask
├── web/                   # Frontend (HTML/CSS/JS)
│   ├── assets/           # Recursos estáticos
│   │   ├── css/          # Estilos
│   │   ├── js/           # JavaScript
│   │   ├── img/          # Imágenes
│   │   └── video/        # Videos
│   ├── components/       # Componentes HTML reutilizables
│   ├── pages/            # Páginas HTML
│   └── index.html        # Página principal
└── db/                   # Scripts de base de datos
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- npm o yarn

### Backend (API)

1. **Instalar dependencias:**
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=tu_password
   DB_PORT=3306
   DB_NAME=sign_technology
   SECRET_KEY=tu_secret_key_segura
   API_PORT=5001
   API_HOST=0.0.0.0
   DEBUG=True
   FRONTEND_URL=http://localhost:3000
   
   # Opcional: Configuración de correo para recuperación de contraseña
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=tu_email@gmail.com
   MAIL_PASSWORD=tu_app_password
   ```

3. **Configurar base de datos:**
   ```bash
   mysql -u root -p < db/sign_technology.sql
   ```

4. **Ejecutar la API:**
   ```bash
   cd api
   python app_api.py
   ```

   La API estará disponible en: `http://localhost:5001`

### Frontend (Web)

1. **Instalar dependencias:**
   ```bash
   cd web
   npm install
   ```

2. **Compilar CSS (modo desarrollo con watch):**
   ```bash
   npm run dev
   ```

3. **Compilar CSS (producción):**
   ```bash
   npm run build
   ```

4. **Iniciar servidor local:**
   ```bash
   npm run server
   ```

   El frontend estará disponible en: `http://localhost:3000` (o el puerto que asigne `serve`)

## 📚 Endpoints de la API

### Autenticación (`/api/auth`)
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/verificar-token` - Verificar token JWT
- `POST /api/auth/logout` - Cerrar sesión
- `POST /api/auth/forgot-password` - Solicitar recuperación de contraseña
- `POST /api/auth/reset-password` - Restablecer contraseña
- `POST /api/auth/verify-reset-token` - Verificar token de recuperación

### Administración (`/api/admin`)
- `GET /api/admin/stats/estadisticas` - Estadísticas del dashboard
- `GET /api/admin/usuarios` - Listar usuarios (solo admin)
- `POST /api/admin/usuarios` - Crear usuario (solo admin)
- `GET /api/admin/perfil` - Obtener perfil del usuario actual
- `PUT /api/admin/perfil` - Actualizar perfil
- `GET /api/admin/reportes` - Listar reportes
- `GET /api/admin/contribuciones` - Listar contribuciones

Ver `api/app_api.py` para la lista completa de endpoints.

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web
- **PyMySQL** - Cliente MySQL
- **JWT** - Autenticación
- **bcrypt** - Hash de contraseñas
- **Flask-CORS** - Manejo de CORS

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **Tailwind CSS** - Framework CSS utility-first
- **JavaScript (Vanilla)** - Lógica del frontend
- **Font Awesome** - Iconos

## 📝 Notas de Desarrollo

### Estructura de Archivos JavaScript

- `assets/js/services/` - Servicios (API, etc.)
- `assets/js/controllers/` - Controladores de páginas
- `assets/js/components/` - Componentes reutilizables
- `assets/js/utils/` - Utilidades y helpers
- `assets/js/pages/` - Scripts específicos de páginas

### Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación. Los tokens deben enviarse en el header:
```
Authorization: Bearer <token>
```

### Base de Datos

El esquema de la base de datos está en `db/sign_technology.sql`. Las tablas principales son:
- `usuarios` - Usuarios del sistema
- `roles` - Roles (Administrador, Colaborador)
- `contribuciones_senas` - Contribuciones de señas
- `reportes_errores` - Reportes de errores
- `traducciones` - Historial de traducciones

## 🔒 Seguridad

- Las contraseñas se hashean con bcrypt
- Los tokens JWT tienen expiración
- Validación de roles en endpoints sensibles
- CORS configurado (ajustar para producción)

## 📄 Licencia

ISC

## 👥 Contribuidores

Sign Technology Team

