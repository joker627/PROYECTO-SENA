-- ============================================================
-- 📦 BASE DE DATOS: sign_technology
-- Versión final integrada con reportes de errores
-- Fecha: 2025-11-08
-- ============================================================

CREATE DATABASE IF NOT EXISTS sign_technology;
USE sign_technology;

-- ============================================================
-- 1️⃣ ROLES Y USUARIOS
-- ============================================================
CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre ENUM('ADMINISTRADOR', 'GESTOR') UNIQUE NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    estado ENUM('ACTIVO','INACTIVO') DEFAULT 'ACTIVO',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- ============================================================
-- 2️⃣ USUARIOS ANÓNIMOS
-- ============================================================
CREATE TABLE usuarios_anonimos (
    id_anonimo INT AUTO_INCREMENT PRIMARY KEY,
    uuid_transaccion CHAR(36) UNIQUE NOT NULL,
    ip_usuario VARCHAR(45),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3️⃣ SOLICITUDES DE COLABORACIÓN
-- ============================================================
CREATE TABLE solicitudes_colaboracion (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_anonimo INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    motivacion TEXT NOT NULL,
    ejemplo_media TEXT,
    estado ENUM('pendiente','aceptado') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_revisor INT NULL,
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo),
    FOREIGN KEY (id_revisor) REFERENCES usuarios(id_usuario)
);

-- ============================================================
-- 4️⃣ CONTRIBUCIONES DE SEÑAS (subidas por anónimos)
-- ============================================================
CREATE TABLE contribuciones_senas (
    id_contribucion INT AUTO_INCREMENT PRIMARY KEY,
    id_anonimo INT NOT NULL COMMENT 'Usuario anónimo que sube la seña',
    correo_respuesta VARCHAR(120) NULL COMMENT 'Correo opcional para notificaciones',
    descripcion TEXT NOT NULL COMMENT 'Descripción o palabra/frase representada (ej: hola)',
    archivo_media TEXT NOT NULL COMMENT 'Ruta o URL del video subido (temporal)',
    estado ENUM('pendiente','validada','rechazada') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_validador INT NULL COMMENT 'Gestor o admin que valida',
    fecha_validacion TIMESTAMP NULL,
    ruta_dataset TEXT NULL COMMENT 'Ruta final en dataset oficial (si se validó)',
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo) ON DELETE CASCADE,
    FOREIGN KEY (id_validador) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 5️⃣ REPOSITORIO OFICIAL DE SEÑAS (solo texto → seña)
-- ============================================================
CREATE TABLE repositorio_senas (
    id_repositorio INT AUTO_INCREMENT PRIMARY KEY,
    texto_asociado VARCHAR(255) NOT NULL COMMENT 'Texto que representa la seña, ej: "hola"',
    url_video TEXT NOT NULL COMMENT 'Video oficial de la seña (ruta definitiva)',
    descripcion TEXT COMMENT 'Contexto o uso breve',
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_validador INT NULL COMMENT 'Usuario que aprobó la seña',
    id_origen INT NULL COMMENT 'id_contribucion de donde vino (si aplica)',
    FOREIGN KEY (id_validador) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_origen) REFERENCES contribuciones_senas(id_contribucion) ON DELETE SET NULL
);

-- ============================================================
-- 6️⃣ ALERTAS DEL SISTEMA
-- ============================================================
CREATE TABLE alertas_sistema (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    modulo VARCHAR(100) NOT NULL,
    tipo_error VARCHAR(100) NOT NULL,
    severidad ENUM('bajo','medio','alto','critico') NOT NULL,
    origen_sistema VARCHAR(100),
    funcion_fallida VARCHAR(150),
    descripcion TEXT,
    hash_error CHAR(32) UNIQUE NOT NULL,
    contador_ocurrencias INT DEFAULT 1,
    ultima_ocurrencia TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    estado ENUM('pendiente','en revision','resuelto') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion TIMESTAMP NULL,
    id_responsable INT NULL,
    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 7️⃣ REPORTES DE ERRORES (por anónimos o por usuario registrado)
-- ============================================================
CREATE TABLE reportes_error (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_anonimo INT NULL COMMENT 'Si fue reportado por un anónimo',
    id_usuario INT NULL COMMENT 'Si fue reportado por un usuario logueado',
    tipo_error VARCHAR(120),
    descripcion TEXT,
    evidencia_url TEXT,
    id_traduccion INT NULL COMMENT 'Referencia a traducción relacionada (si aplica)',
    origen ENUM('texto_a_sena','sena_a_texto') NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente','en revision','resuelto') DEFAULT 'pendiente',
    fecha_resolucion TIMESTAMP NULL,
    id_responsable INT NULL COMMENT 'Usuario que atendió el reporte',
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);


CREATE TABLE rendimiento_modelo (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    precision_promedio DECIMAL(5,2) NOT NULL COMMENT 'Precisión general del modelo de seña a texto',
    muestras_usadas INT DEFAULT 0 COMMENT 'Cantidad de pruebas usadas para calcular el promedio',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 8️⃣ DATOS INICIALES (roles + ejemplo de usuarios)
-- ============================================================
INSERT INTO roles (nombre, descripcion)
VALUES 
('ADMINISTRADOR', 'Control total del sistema'),
('GESTOR', 'Administra y valida contribuciones');

INSERT INTO usuarios (nombre, correo, contrasena, id_rol, estado)
VALUES 
('Administrador General', 'admin@signtech.com', 'admin123', 1, 'ACTIVO'),
('Gestor Principal', 'gestor@signtech.com', 'gestor123', 2, 'ACTIVO');
