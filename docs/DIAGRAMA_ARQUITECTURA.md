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
│  • layout.html          │  • Email │                         │
│  • newsletter templates │  • Glob. │                         │
└─────────────────────────────────────────────────────────────┘
                                ↕️ HTTP Requests
┌─────────────────────────────────────────────────────────────┐
│                   🌶️ FLASK APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                       🚀 main.py                           │
│              • Configuración de la app                     │
│              • Registro de Blueprints                      │
│              • Gestión de sesiones                         │
│              • Configuración SMTP                          │
└─────────────────────────────────────────────────────────────┘
                                ↕️
┌─────────────────────────────────────────────────────────────┐
│                   🛤️ ROUTES (Blueprints)                   │
├─────────────────────────────────────────────────────────────┤
│  📁 auth/           │  📁 profile_routes.py │  📁 routes.py  │
│  • /auth/login      │  • /profile/          │  • /          │
│  • /auth/logout     │  • /profile/update-*  │  • /dashboard │
│  • /auth/register   │  • /profile/change-*  │  • /newsletter│
│                     │  • /profile/delete-*  │               │
└─────────────────────────────────────────────────────────────┘
                                ↕️ Calls
┌─────────────────────────────────────────────────────────────┐
│                  🎮 CONTROLLERS (Business Logic)           │
├─────────────────────────────────────────────────────────────┤
│   AuthController   │   ProfileController   │ NewsletterCtrl │
│  ┌───────────────┐ │ ┌───────────────────┐ │ ┌─────────────┐ │
│  │ • login_user()│ │ │ • get_user_prof. │ │ │ • subscribe │ │
│  │ • logout_user│ │ │ • update_usernam │ │ │ • confirm   │ │
│  │ • register   │ │ │ • update_email() │ │ │ • unsubscri │ │
│  │ • require_log│ │ │ • change_passw. │ │ │             │ │
│  │ • get_current│ │ │ • delete_account │ │ │             │ │
│  └───────────────┘ │ └───────────────────┘ │ └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                ↕️
┌─────────────────────────────────────────────────────────────┐
│                    📧 SERVICES LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  EmailService (SMTP)   │  TranslatorService  │  VideoUtils  │
│  ┌─────────────────┐   │  ┌─────────────────┐ │ ┌──────────┐ │
│  │ • send_welcome  │   │  │ • translate_txt │ │ │ • process│ │
│  │ • send_passw_ch │   │  │ • text_to_sign  │ │ │ • convert│ │
│  │ • send_deletion │   │  │ • sign_to_text  │ │ │          │ │
│  │ • send_newslett │   │  │                 │ │ │          │ │
│  │ (Gmail SMTP)    │   │  │                 │ │ │          │ │
│  └─────────────────┘   │  └─────────────────┘ │ └──────────┘ │
└─────────────────────────────────────────────────────────────┘
                                ↕️ Data Operations
┌─────────────────────────────────────────────────────────────┐
│                   🗃️ MODELS (Data Access Layer)            │
├─────────────────────────────────────────────────────────────┤
│      user_model.py     │         newsletter_model.py       │
│  ┌───────────────────┐ │  ┌───────────────────────────────┐ │
│  │ • get_user_by_em. │ │  │ • add_subscriber()           │ │
│  │ • get_user_by_id()│ │  │ • email_exists()             │ │
│  │ • create_user()   │ │  │ • confirm_subscription()     │ │
│  │ • update_usernam. │ │  │ • unsubscribe_email()        │ │
│  │ • update_email()  │ │  │ • get_all_subscribers()      │ │
│  │ • verify_password │ │  │                               │ │
│  │ • get_all_roles()         • change_user_password()     │ │
│  │ • delete_user_account()   • (Hash/Verify passwords)    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                ↕️ SQL Queries
┌─────────────────────────────────────────────────────────────┐
│                    🗄️ DATABASE (MySQL)                      │
├─────────────────────────────────────────────────────────────┤
│   👥 usuarios         🎭 roles         📧 newsletter_emails│
│ ┌─────────────────┐ ┌─────────────┐ ┌────────────────────┐  │
│ │ id_usuario (PK) │ │ id_rol (PK) │ │ id (PK)           │  │
│ │ nombre          │◄┐│ nombre_rol  │ │ email (UNIQUE)    │  │
│ │ correo (UNIQUE) │ ├│ descripcion │ │ fecha_suscripcion │  │
│ │ contrasena (HAS)│ ││             │ │ confirmado (BOOL) │  │
│ │ fecha_registro  │ ││             │ │ token_confirmacion│  │
│ │ id_rol (FK) ────┼─┘│             │ │                   │  │
│ └─────────────────┘  └─────────────┘ └────────────────────┘  │
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
bcrypt.hash() → MySQL UPDATE → EmailService.send_password_change() → Gmail SMTP
    ↓
Session Update → Response
```

### 4. 📧 Suscripción a Newsletter
```
Formulario → /newsletter → NewsletterController.subscribe()
    ↓
Validación email → newsletter_model.add_subscriber() → MySQL INSERT
    ↓
EmailService.send_newsletter_confirmation() → Gmail SMTP → Email enviado
    ↓
Response → Flash Message → Redirect
```

### 5. 📤 Registro de Usuario
```
register.html → /auth/register → AuthController.register_new_user()
    ↓
Validaciones → UserModel.create_user() → MySQL INSERT
    ↓
EmailService.send_welcome_email() → Gmail SMTP → Email bienvenida
    ↓
Session → Flash Message → Redirect → Login
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