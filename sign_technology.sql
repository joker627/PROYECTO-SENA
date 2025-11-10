-- ============================================================
--  BASE DE DATOS: sign_technology
-- Versión final optimizada:
-- Fecha: 2025-11-10
-- ============================================================

CREATE DATABASE IF NOT EXISTS sign_technology;
USE sign_technology;

-- ============================================================
-- 1 ROLES Y USUARIOS
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
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    estado ENUM('ACTIVO','INACTIVO') DEFAULT 'ACTIVO',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- ============================================================
-- 2 USUARIOS ANÓNIMOS (solo donde se necesita rastreo)
-- ============================================================
CREATE TABLE usuarios_anonimos (
    id_anonimo INT AUTO_INCREMENT PRIMARY KEY,
    uuid_transaccion CHAR(36) UNIQUE NOT NULL,
    ip_usuario VARCHAR(45) NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3 SOLICITUDES DE COLABORACIÓN (puede ser anónimo)
-- ============================================================
CREATE TABLE solicitudes_colaboracion (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_anonimo INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    motivacion TEXT NOT NULL,
    estado ENUM('pendiente','aceptado') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_revisor INT NULL,
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo),
    FOREIGN KEY (id_revisor) REFERENCES usuarios(id_usuario)
);

-- ============================================================
-- 4 CONTRIBUCIONES DE SEÑAS (cualquiera puede subir)
-- ============================================================
CREATE TABLE contribuciones_senas (
    id_contribucion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_contribuyente VARCHAR(100) NULL COMMENT 'Nombre opcional del que sube la seña',
    correo_respuesta VARCHAR(120) NULL COMMENT 'Correo opcional para notificaciones',
    descripcion TEXT NOT NULL COMMENT 'Descripción o palabra/frase representada',
    archivo_media TEXT NOT NULL COMMENT 'Ruta o URL del video subido',
    estado ENUM('pendiente','validada','rechazada') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_validador INT NULL COMMENT 'Colaborador o admin que valida',
    fecha_validacion TIMESTAMP NULL,
    ruta_dataset TEXT NULL COMMENT 'Ruta final en dataset oficial',
    FOREIGN KEY (id_validador) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 5 REPOSITORIO OFICIAL DE SEÑAS (solo colaboradores/admins)
-- ============================================================
CREATE TABLE repositorio_senas (
    id_repositorio INT AUTO_INCREMENT PRIMARY KEY,
    texto_asociado VARCHAR(255) NOT NULL COMMENT 'Texto que representa la seña',
    url_video TEXT NOT NULL COMMENT 'Video oficial de la seña',
    descripcion TEXT COMMENT 'Contexto o uso breve',
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_validador INT NULL COMMENT 'Colaborador o admin que aprobó',
    id_origen INT NULL COMMENT 'id_contribucion de donde vino',
    FOREIGN KEY (id_validador) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_origen) REFERENCES contribuciones_senas(id_contribucion) ON DELETE SET NULL
);

-- ============================================================
-- 6 ALERTAS DEL SISTEMA
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
    estado ENUM('pendiente','en revision') DEFAULT 'pendiente',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_responsable INT NULL,
    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 7 REPORTES DE ERRORES (universal, evidencia obligatoria)
-- ============================================================
CREATE TABLE reportes_error (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    nombre_reportante VARCHAR(100) NULL COMMENT 'Nombre opcional del que reporta',
    correo_contacto VARCHAR(120) NULL COMMENT 'Correo opcional de contacto',
    tipo_error VARCHAR(120) NOT NULL COMMENT 'Tipo o categoría del error',
    descripcion TEXT NOT NULL COMMENT 'Descripción detallada del error',
    evidencia_url TEXT NOT NULL COMMENT 'URL o ruta a evidencia (obligatoria)',
    id_traduccion INT NULL COMMENT 'Referencia a traducción relacionada',
    origen ENUM('texto_a_sena','sena_a_texto') NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente','en revision') DEFAULT 'pendiente',
    fecha_resolucion TIMESTAMP NULL,
    id_responsable INT NULL COMMENT 'Colaborador o admin que revisa o resuelve el error',
    FOREIGN KEY (id_responsable) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 8 RENDIMIENTO DEL MODELO
-- ============================================================
CREATE TABLE rendimiento_modelo (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    precision_promedio DECIMAL(5,2) NOT NULL COMMENT 'Precisión general del modelo de seña a texto',
    muestras_usadas INT DEFAULT 0 COMMENT 'Cantidad de pruebas usadas',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 9 DATOS INICIALES
-- ============================================================
INSERT INTO roles (nombre, descripcion)
VALUES 
('ADMINISTRADOR', 'Control total del sistema'),
('COLABORADOR', 'Administra y valida contribuciones');

INSERT INTO usuarios (nombre, correo, contrasena, id_rol, estado)
VALUES 
('Administrador General', 'manuelx6@gmail.com', 'admin123', 1, 'ACTIVO'),
('Colaborador Principal', 'colaborador@signtech.com', 'colab123', 2, 'ACTIVO');
