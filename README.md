# 🤟 PROYECTO SENA - Intérprete de Lenguaje de Señas Colombianas

<!--h1 without bottom border-->
<div id="user-content-toc">
  <ul align="center">
    <summary><h1 style="display: inline-block"> 🤟 Intérprete de Lenguaje de Señas Colombianas (LSC) </h1></summary>
  </ul>
</div>

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 🎯 Misión del Proyecto
*"Desarrollar un software que intérprete lenguaje de señas colombiana, para facilitar la comunicación con la comunidad con discapacidad auditiva en Colombia, promoviendo su inclusión social en el campo laboral o académico."*

## 🏗️ Arquitectura & Tecnologías

### 💻 Stack Tecnológico
- **🐍 Backend**: Python 3.x + Flask (MVC Architecture)
- **🎨 Frontend**: HTML5 + CSS3 (Grid/Flexbox) + JavaScript (Minimal)
- **🗄️ Database**: MySQL 8.0+ con PyMySQL
- **🔐 Seguridad**: bcrypt para hashing de contraseñas
- **📋 Templates**: Jinja2 para renderizado dinámico

### 📚 Documentación Completa

| 📖 Documento | 📝 Descripción | 🔗 Enlace |
|--------------|----------------|-----------|
| **🏗️ Arquitectura** | Estructura completa del sistema, diagramas y flujos | [`DOCUMENTACION_ESTRUCTURA.md`](./DOCUMENTACION_ESTRUCTURA.md) |
| **📊 Diagramas** | Diagramas visuales de arquitectura y flujo de datos | [`DIAGRAMA_ARQUITECTURA.md`](./DIAGRAMA_ARQUITECTURA.md) |
| **🚀 Guía de Desarrollo** | Setup, patrones de código y mejores prácticas | [`GUIA_DESARROLLO.md`](./GUIA_DESARROLLO.md) |
| **📋 Dependencias** | Lista completa de librerías Python | [`requirements.txt`](./requirements.txt) |

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>


Este es un proyecto de software desarrollado con fines educativos, de investigación y de impacto social.  
Su propósito es aportar valor como herramienta abierta y colaborativa, **sin fines comerciales**.

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 🚀 Quick Start

### ⚡ Instalación Rápida
```bash
# 1. Clonar el repositorio
git clone [repository-url]
cd PROYECTO-SENA

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos (editar backend/config/conexion.py)

# 4. Ejecutar la aplicación
cd backend
python main.py
```

### 🌐 Acceso
- **🏠 Aplicación**: `http://localhost:5000`
- **🔐 Login**: `http://localhost:5000/auth/login`
- **👤 Perfil**: `http://localhost:5000/profile`

## 🎯 Funcionalidades Principales

### ✨ Sistema de Usuario
- 🔐 **Autenticación segura** con bcrypt
- 👤 **Gestión de perfil** completa
- 🔄 **Cambio de contraseña** con validaciones
- 📧 **Actualización de datos** personales

### 🤟 Traducción de Señas (En Desarrollo)
- 📹 **Video a Texto** - Interpretación de señas colombianas
- 📝 **Texto a Video** - Generación de señas
- 🎯 **Reconocimiento en tiempo real**

## 🏗️ Arquitectura del Sistema

```
🌐 Frontend (Templates + CSS + JS)
         ↕️
🛤️ Routes (Flask Blueprints)
         ↕️  
🎮 Controllers (Business Logic)
         ↕️
🗃️ Models (Database Access)
         ↕️
🗄️ MySQL Database
```

### 📁 Estructura Organizada
- **`backend/controllers/`** - Lógica de negocio centralizada
- **`backend/routes/`** - Endpoints organizados por funcionalidad  
- **`backend/models/`** - Acceso a base de datos
- **`frontend/templates/`** - Interfaces HTML con Jinja2
- **`frontend/static/`** - CSS, JavaScript e imágenes

## 🚀 Objetivo
Brindar una base tecnológica abierta para el aprendizaje y la innovación, garantizando que cualquier persona pueda **usar, estudiar y mejorar** este software, pero **sin obtener lucro directo** ni apropiarse indebidamente del trabajo.

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 📜 Licencia
Este software está protegido bajo la licencia **No Profit Open License (NPOL-2025)**, inspirada en MIT pero con cláusulas adicionales para mayor seguridad legal.  

- ✔️ Se permite **usar, y contribuir** el software en cualquier parte del mundo.  
- ❌ **Prohibido lucrar, vender, distribuir o monetizar** este software o derivados directos.  
- ✔️ Puedes contribuir y mejorar el proyecto, siempre manteniendo abierto y gratuito el resultado.  
- ❌ No se permite registrar patentes, marcas o derechos exclusivos basados en este software.  

El incumplimiento de estas condiciones puede conllevar **acciones legales internacionales**, respaldadas por los derechos de autor y tratados de propiedad intelectual.

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## ⚖️ Responsabilidad
El software se proporciona **“tal cual”**, sin garantía de ningún tipo.  
Los autores no se hacen responsables por:  
- Daños directos o indirectos derivados del uso.  
- Malas implementaciones por terceros.  
- Cualquier intento de explotación indebida.  

El uso de este software implica la aceptación total de estas condiciones.

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 🌍 Alcance Global
Este proyecto se encuentra amparado bajo tratados internacionales de propiedad intelectual (Convenio de Berna, ADPIC/TRIPS y otros), por lo que **su validez es mundial**.  

En palabras simples: **libre y abierto sí, pero nunca para que alguien lo use como negocio privado**.  

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 🤝 Contribuciones
Se aceptan aportes siempre que respeten la filosofía del proyecto.  
Toda contribución será de carácter **abierto, gratuito y no lucrativo**.

<a href=""><img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"></a>

## 📩 Colaboradores   

<div align="center" style="display:flex; justify-content:center; align-items:center; gap:50px; margin-top:20px;">

  <!-- Manuel -->
  <a href="https://github.com/joker627" target="_blank" style="text-decoration:none; text-align:center; color:inherit;">
    <div style="width:85px; height:85px; border-radius:50%; overflow:hidden; border:2px solid #444; box-shadow:0 3px 8px rgba(0,0,0,0.25); margin:auto;">
      <img src="https://github.com/joker627.png" 
           alt="joker627" 
           style="width:100%; height:100%; object-fit:cover;"/>
    </div>
    <br>
    <span style="font-size:13px; font-weight:600; font-family:Segoe UI, sans-serif; color:#4ade80;">Manuel-Dev</span>
  </a>

  <!-- Miguel -->
  <a href="https://github.com/miguelprograma200" target="_blank" style="text-decoration:none; text-align:center; color:inherit;">
    <div style="width:85px; height:85px; border-radius:50%; overflow:hidden; border:2px solid #444; box-shadow:0 3px 8px rgba(0,0,0,0.25); margin:auto;">
      <img src="https://github.com/miguelprograma200.png" 
           alt="miguelprograma200" 
           style="width:100%; height:100%; object-fit:cover;"/>
    </div>
    <br>
    <span style="font-size:13px; font-weight:600; font-family:Segoe UI, sans-serif; color:#3da9fc;">miguelprograma200</span>
  </a>

</div>
<p align="center"><b>📅 Año: 2025</b></p> 

