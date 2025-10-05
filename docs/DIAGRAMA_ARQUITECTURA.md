# 🏗️ Diagrama de Arquitectura - PROYECTO SENA

## 📊 Arquitectura Completa del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 FRONTEND (Cliente)                     │
├─────────────────────────────────────────────────────────────┤
│  📄 Templates (Jinja2)  │  🎨 CSS  │  ⚡ JavaScript (Mínimo)  │
│  • login.html           │  • Grid  │  • profile.js           │
│  • register.html        │  • Flex  │  • script.js            │
│  • profile/index.html   │  • Resp. │  • modos_traduccion.js  │
│  • layout.html          │         │                         │
└─────────────────────────────────────────────────────────────┘
                                ↕️ HTTP Requests
┌─────────────────────────────────────────────────────────────┐
│                   🌶️ FLASK APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                       🚀 main.py                           │
│              • Configuración de la app                     │
│              • Registro de Blueprints                      │
│              • Gestión de sesiones                         │
└─────────────────────────────────────────────────────────────┘
                                ↕️
┌─────────────────────────────────────────────────────────────┐
│                   🛤️ ROUTES (Blueprints)                   │
├─────────────────────────────────────────────────────────────┤
│  📁 auth/           │  📁 profile_routes.py │  📁 routes.py  │
│  • /auth/login      │  • /profile/          │  • /          │
│  • /auth/logout     │  • /profile/update-*  │  • /dashboard │
│  • /auth/register   │  • /profile/change-*  │               │
│                     │  • /profile/delete-*  │               │
└─────────────────────────────────────────────────────────────┘
                                ↕️ Calls
┌─────────────────────────────────────────────────────────────┐
│                  🎮 CONTROLLERS (Business Logic)           │
├─────────────────────────────────────────────────────────────┤
│        AuthController        │       ProfileController       │
│    ┌─────────────────────┐   │   ┌─────────────────────────┐ │
│    │ • login_user()      │   │   │ • get_user_profile()   │ │
│    │ • logout_user()     │   │   │ • update_username()    │ │
│    │ • register_new_user│   │   │ • update_email()       │ │
│    │ • require_login()   │   │   │ • change_password()    │ │
│    │ • get_current_user()│   │   │ • delete_account()     │ │
│    └─────────────────────┘   │   └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                ↕️ Data Operations
┌─────────────────────────────────────────────────────────────┐
│                   🗃️ MODELS (Data Access Layer)            │
├─────────────────────────────────────────────────────────────┤
│                      user_model.py                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • get_user_by_email()     • update_user_username()     │ │
│  │ • get_user_by_id()        • update_user_email()        │ │
│  │ • create_user()           • verify_current_password()  │ │
│  │ • get_all_roles()         • change_user_password()     │ │
│  │ • delete_user_account()   • (Hash/Verify passwords)    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                ↕️ SQL Queries
┌─────────────────────────────────────────────────────────────┐
│                    🗄️ DATABASE (MySQL)                      │
├─────────────────────────────────────────────────────────────┤
│     👥 usuarios                    🎭 roles                │
│  ┌─────────────────────┐      ┌─────────────────────────┐   │
│  │ id_usuario (PK)     │      │ id_rol (PK)            │   │
│  │ nombre              │◄────┐│ nombre_rol             │   │
│  │ correo (UNIQUE)     │     ├│ descripcion            │   │
│  │ contrasena (HASHED) │     ││                        │   │
│  │ fecha_registro      │     ││                        │   │
│  │ id_rol (FK) ────────┼─────┘│                        │   │
│  └─────────────────────┘      └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

## 🔄 Flujo de Datos Detallado

### 1. 📤 Petición de Login
```
Usuario → login.html → /auth/login → AuthController.login_user() 
    ↓
UserModel.get_user_by_email() → MySQL → Verificación → Sesión
    ↓
Respuesta → Flash Message → Redirect → Dashboard
```

### 2. 👤 Gestión de Perfil
```
Usuario → profile/index.html → /profile/update-username → ProfileController
    ↓
require_login() → update_username() → UserModel.update_user_username()
    ↓
MySQL UPDATE → Success/Error → Flash Message → Redirect
```

### 3. 🔐 Cambio de Contraseña
```
Formulario → /profile/change-password → ProfileController.change_password()
    ↓
Validaciones → verify_current_password() → change_user_password()
    ↓
bcrypt.hash() → MySQL UPDATE → Session Update → Response
```

## 🏗️ Principios de Arquitectura Aplicados

### 🎯 Single Responsibility Principle (SRP)
- **Routes**: Solo manejan HTTP requests/responses
- **Controllers**: Solo lógica de negocio
- **Models**: Solo acceso a datos
- **Templates**: Solo presentación

### 🔄 Dependency Inversion Principle (DIP)
- **Controllers** dependen de abstracciones (Models)
- **Routes** dependen de abstracciones (Controllers)
- **Fácil testing** y mantenimiento

### 📦 Separation of Concerns
- **Presentación**: Templates + CSS + JS
- **Lógica**: Controllers
- **Datos**: Models + Database
- **Configuración**: Config files

## 🛡️ Flujo de Seguridad

```
┌─────────────────┐    🔐 Hash     ┌─────────────────┐
│   Password      │─────────────→  │   bcrypt.hash   │
│   Plaintext     │                │   (Stored)      │
└─────────────────┘                └─────────────────┘
         ↓                                   ↑
    🔍 Login                            💾 Register
         ↓                                   ↑
┌─────────────────┐    ✅ Compare   ┌─────────────────┐
│ bcrypt.checkpw  │←──────────────  │   User Input    │
│ (Verification)  │                 │   + Hash DB     │
└─────────────────┘                 └─────────────────┘
         ↓
    🎫 Session Created
         ↓
    🛡️ Protected Routes
```

## 📱 Responsive Design Structure

```
┌─────────────────────────────────────────┐
│  📱 Mobile (< 768px)    │ 💻 Desktop     │
├─────────────────────────────────────────┤
│  • Stack layout        │ • Grid layout  │
│  • Collapsible menu    │ • Sidebar      │
│  • Touch-friendly      │ • Hover states │
│  • Single column       │ • Multi-column │
└─────────────────────────────────────────┘
```

---

*🏗️ Esta arquitectura garantiza:*
- ✅ **Escalabilidad** - Fácil agregar nuevas funcionalidades
- ✅ **Mantenibilidad** - Código organizado y separado
- ✅ **Testabilidad** - Componentes independientes
- ✅ **Seguridad** - Mejores prácticas implementadas
- ✅ **Performance** - Estructura optimizada