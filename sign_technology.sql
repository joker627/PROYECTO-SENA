-- ============================================================
-- 📦 BASE DE DATOS: sign_technology
-- Versión final IA + manual, con usuarios anónimos
-- ============================================================

CREATE DATABASE IF NOT EXISTS sign_technology;
USE sign_technology;

-- ============================================================
-- 1️⃣ ROLES
-- ============================================================
CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

INSERT INTO roles (nombre_rol)
VALUES ('Administrador'), ('Colaborador');

-- ============================================================
-- 2️⃣ USUARIOS
-- ============================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT DEFAULT 2,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- ============================================================
-- 2️⃣a USUARIOS ANÓNIMOS
-- ============================================================
CREATE TABLE usuarios_anonimos (
    id_anonimo INT AUTO_INCREMENT PRIMARY KEY,
    uuid_visitante CHAR(36) NOT NULL UNIQUE COMMENT 'UUID único del visitante',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3️⃣ TRADUCCIONES
-- ============================================================
CREATE TABLE traducciones (
    id_traduccion INT AUTO_INCREMENT PRIMARY KEY,
    tipo_traduccion ENUM('texto_a_senas', 'senas_a_texto') NOT NULL COMMENT 'Manual o IA',
    texto_entrada TEXT NULL COMMENT 'Solo se guarda si es manual (texto → seña)',
    enlace_sena_entrada VARCHAR(255) NULL COMMENT 'Enlace al video si es traducción de texto → seña',
    resultado_salida TEXT NOT NULL COMMENT 'Texto resultante o descripción del resultado',
    fallo BOOLEAN DEFAULT FALSE COMMENT 'Si la traducción manual tuvo error',
    fecha_traduccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT NULL,
    id_anonimo INT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo)
);

-- ============================================================
-- 4️⃣ CONTRIBUCIONES
-- ============================================================
CREATE TABLE contribuciones (
    id_contribucion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NULL,
    id_anonimo INT NULL,
    descripcion TEXT NOT NULL,
    archivo_prueba VARCHAR(255) COMMENT 'Video o imagen de la seña aportada',
    estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo)
);

-- ============================================================
-- 5️⃣ SOLICITUDES DE COLABORADOR
-- ============================================================
CREATE TABLE solicitudes_colaborador (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'aceptada', 'rechazada') DEFAULT 'pendiente'
);

-- ============================================================
-- 6️⃣ REPORTES DE ERRORES
-- ============================================================
CREATE TABLE reportes_errores (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_traduccion INT NULL COMMENT 'Referencia a traducción relacionada si aplica',
    tipo_traduccion ENUM('texto_a_senas','senas_a_texto') COMMENT 'Tipo de traducción que generó el error',
    descripcion_error TEXT NOT NULL COMMENT 'Detalle del error o fallo detectado',
    evidencia_url VARCHAR(255) NOT NULL COMMENT 'Captura o referencia obligatoria del fallo',
    prioridad ENUM('baja', 'media', 'alta') DEFAULT 'media',
    estado ENUM('pendiente','en_revision') DEFAULT 'pendiente',
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_traduccion) REFERENCES traducciones(id_traduccion)
);

-- ============================================================
-- 7️⃣ REPOSITORIO DE SEÑAS (dataset oficial)
-- ============================================================
CREATE TABLE repositorio_senas (
    id_sena INT AUTO_INCREMENT PRIMARY KEY,
    palabra_asociada VARCHAR(100) NOT NULL,
    archivo_video VARCHAR(255) NOT NULL COMMENT 'Video oficial de la seña',
    validada BOOLEAN DEFAULT FALSE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8️⃣ RENDIMIENTO DEL MODELO IA
-- ============================================================
CREATE TABLE rendimiento_modelo (
    id_rendimiento INT AUTO_INCREMENT PRIMARY KEY,
    precision_actual DECIMAL(5,2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT
);

-- ============================================================
-- 9️⃣ ESTADÍSTICAS GLOBALES (panel admin)
-- ============================================================
CREATE TABLE estadisticas (
    id_estadistica INT AUTO_INCREMENT PRIMARY KEY,
    total_traducciones INT DEFAULT 0,
    traducciones_texto_a_senas INT DEFAULT 0,
    traducciones_senas_a_texto INT DEFAULT 0,
    errores_reportados INT DEFAULT 0,
    contribuciones_pendientes INT DEFAULT 0,
    contribuciones_aprobadas INT DEFAULT 0,
    precision_modelo DECIMAL(5,2) DEFAULT 0.00,
    senas_validadas INT DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- 🔑 TOKENS DE RECUPERACIÓN DE CONTRASEÑA
-- ============================================================
CREATE TABLE tokens_recuperacion (
    id_token INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE COMMENT 'Token seguro para recuperación de contraseña',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL COMMENT 'Válido 1 hora desde creación',
    usado BOOLEAN DEFAULT FALSE COMMENT 'Evita reutilización del token',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
