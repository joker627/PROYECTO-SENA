-- ============================================================ 

-- 📦 BASE DE DATOS: sign_technology 

-- Versión final: sistema usado solo por usuarios anónimos 

-- Roles gestionan el contenido, no lo usan 

-- Fecha: 2025-11-04 

-- ============================================================ 

  

CREATE DATABASE IF NOT EXISTS sign_technology; 

USE sign_technology; 

  

-- ============================================================ 

-- 1️⃣ ROLES Y USUARIOS (solo administrativos) 

-- ============================================================ 

  

CREATE TABLE roles ( 

    id_rol INT AUTO_INCREMENT PRIMARY KEY, 

    nombre ENUM('ADMINISTRADOR', 'COLABORADOR') UNIQUE NOT NULL, 

    descripcion TEXT, 

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP 

); 

  

CREATE TABLE usuarios ( 

    id_usuario INT AUTO_INCREMENT PRIMARY KEY, 

    nombre VARCHAR(100) NOT NULL, 

    correo VARCHAR(120) UNIQUE NOT NULL, 

    contraseña VARCHAR(255) NOT NULL, 

    id_rol INT NOT NULL, 

    estado ENUM('ACTIVO','INACTIVO','ELIMINADO') DEFAULT 'ACTIVO', 

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) 

); 

  

CREATE TABLE tokens_recuperacion ( 

    id_token INT AUTO_INCREMENT PRIMARY KEY, 

    id_usuario INT NOT NULL, 

    token VARCHAR(255) NOT NULL, 

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    expiracion DATETIME NOT NULL, 

    usado BOOLEAN DEFAULT FALSE, 

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 

); 

  

-- ============================================================ 

-- 2️⃣ USUARIOS ANÓNIMOS (identificados por UUID) 

-- ============================================================ 

  

CREATE TABLE usuarios_anonimos ( 

    id_anonimo INT AUTO_INCREMENT PRIMARY KEY, 

    uuid_transaccion CHAR(36) UNIQUE NOT NULL, 

    ip_usuario VARCHAR(45), 

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP 

); 

  

-- ============================================================ 

-- 3️⃣ MÓDULOS FUNCIONALES (usados solo por usuarios anónimos) 

-- ============================================================ 

  

-- 🔹 Traducción de señas a texto 

CREATE TABLE traducciones_senas_texto ( 

    id_traduccion INT AUTO_INCREMENT PRIMARY KEY, 

    id_anonimo INT NOT NULL, 

    texto_generado TEXT NOT NULL, 

    precision_modelo DECIMAL(5,2), 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo) 

); 

  

-- 🔹 Traducción de texto a señas 

CREATE TABLE traducciones_texto_senas ( 

    id_traduccion INT AUTO_INCREMENT PRIMARY KEY, 

    id_anonimo INT NOT NULL, 

    texto_ingresado TEXT NOT NULL, 

    url_traduccion TEXT NOT NULL, 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo) 

); 

  

-- 🔹 Reporte de errores (anónimo) 

CREATE TABLE reportes_error ( 

    id_reporte INT AUTO_INCREMENT PRIMARY KEY, 

    id_anonimo INT NOT NULL, 

    tipo_error VARCHAR(100), 

    descripcion TEXT, 

    evidencia_url TEXT, 

    id_traduccion INT NULL, 

    origen ENUM('senas_texto', 'texto_senas') NULL, 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    estado ENUM('pendiente','en revisión','resuelto') DEFAULT 'pendiente', 

    id_responsable INT NULL, 

    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo), 

    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) 

); 

  

-- 🔹 Solicitudes para ser colaborador (formulario público) 

CREATE TABLE solicitudes_colaboracion ( 

    id_solicitud INT AUTO_INCREMENT PRIMARY KEY, 

    id_anonimo INT NOT NULL, 

    nombre VARCHAR(100) NOT NULL, 

    correo VARCHAR(120) NOT NULL, 

    motivacion TEXT NOT NULL, 

    ejemplo_media TEXT, 

    estado ENUM('pendiente','aceptado','rechazado') DEFAULT 'pendiente', 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    id_revisor INT NULL, 

    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo), 

    FOREIGN KEY (id_revisor) REFERENCES usuarios(id_usuario) 

); 

  

-- 🔹 Contribuciones de señas (solo COLABORADORES, no anónimos) 

CREATE TABLE contribuciones_senas ( 

    id_contribucion INT AUTO_INCREMENT PRIMARY KEY, 

    id_colaborador INT NOT NULL, 

    descripcion TEXT NOT NULL, 

    archivo_media TEXT NOT NULL, 

    estado ENUM('pendiente','validada','rechazada') DEFAULT 'pendiente', 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    id_validador INT NULL, 

    FOREIGN KEY (id_colaborador) REFERENCES usuarios(id_usuario), 

    FOREIGN KEY (id_validador) REFERENCES usuarios(id_usuario) 

); 

  

-- 🔹 Alertas del sistema (solo administradores) 

CREATE TABLE alertas_sistema ( 

    id_alerta INT AUTO_INCREMENT PRIMARY KEY, 

    modulo ENUM('traducción','almacenamiento','autenticación','otro') NOT NULL, 

    tipo_error VARCHAR(100) NOT NULL, 

    severidad ENUM('bajo','medio','alto','crítico') NOT NULL, 

    descripcion TEXT, 

    estado ENUM('pendiente','en revisión','resuelto') DEFAULT 'pendiente', 

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 

    id_responsable INT NULL, 

    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) 

); 