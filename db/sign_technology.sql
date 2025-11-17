-- ============================================================
--  BASE DE DATOS: sign_technology
-- ============================================================

CREATE DATABASE IF NOT EXISTS sign_technology;
USE sign_technology;

-- ============================================================
-- 1 ROLES
-- ============================================================
CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

INSERT INTO roles (nombre_rol)
VALUES ('Administrador'), ('Colaborador');

-- ============================================================
-- 2 USUARIOS
-- ============================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    id_rol INT DEFAULT 2, -- Colaborador por defecto
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_administrador_aprobo INT NULL COMMENT 'Administrador que aprobó o creó al colaborador',
    
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE RESTRICT,
    FOREIGN KEY (id_administrador_aprobo) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

CREATE INDEX idx_usuarios_correo ON usuarios(correo);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);

-- ============================================================
-- 3 USUARIOS ANÓNIMOS
-- ============================================================
CREATE TABLE usuarios_anonimos (
    id_anonimo INT AUTO_INCREMENT PRIMARY KEY,
    uuid_visitante CHAR(36) NOT NULL UNIQUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 4 CONTRIBUCIONES DE SEÑAS
-- ============================================================
CREATE TABLE contribuciones_senas (
    id_contribucion INT AUTO_INCREMENT PRIMARY KEY,
    palabra_asociada VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    archivo_video VARCHAR(255) NOT NULL,
    id_usuario_gestiono INT NULL COMMENT 'Admin o Colaborador que gestionó',
    estado ENUM('pendiente', 'aprobada') DEFAULT 'pendiente',
    fecha_contribucion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_gestion TIMESTAMP NULL,
    fecha_repositorio TIMESTAMP NULL COMMENT 'Cuando se envió al repositorio oficial',
    observaciones_gestion TEXT NULL,
    
    FOREIGN KEY (id_usuario_gestiono) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

CREATE INDEX idx_contribuciones_estado ON contribuciones_senas(estado);

-- ============================================================
-- 5 REPOSITORIO OFICIAL DE SEÑAS
-- ============================================================
CREATE TABLE repositorio_senas_oficial (
    id_sena INT AUTO_INCREMENT PRIMARY KEY,
    palabra_asociada VARCHAR(100) NOT NULL,
    archivo_video VARCHAR(255) NOT NULL,
    id_contribucion_origen INT NOT NULL,
    id_usuario_valido INT NOT NULL COMMENT 'Admin o Colaborador que validó',
    fecha_validacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_contribucion_origen) REFERENCES contribuciones_senas(id_contribucion) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario_valido) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

CREATE INDEX idx_repositorio_palabra ON repositorio_senas_oficial(palabra_asociada);

-- ============================================================
-- 6 TRADUCCIONES
-- ============================================================
CREATE TABLE traducciones (
    id_traduccion INT AUTO_INCREMENT PRIMARY KEY,
    tipo_traduccion ENUM('texto_a_senas', 'senas_a_texto') NOT NULL,
    texto_entrada TEXT NULL,
    enlace_sena_entrada VARCHAR(255) NULL,
    resultado_salida TEXT NOT NULL,
    fallo BOOLEAN DEFAULT FALSE,
    fecha_traduccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    precision_traduccion DECIMAL(5,2) NULL COMMENT 'Porcentaje de precisión de esta traducción individual',
    id_usuario INT NULL,
    id_anonimo INT NULL,
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    FOREIGN KEY (id_anonimo) REFERENCES usuarios_anonimos(id_anonimo) ON DELETE SET NULL
);

CREATE INDEX idx_traducciones_tipo ON traducciones(tipo_traduccion);

-- ============================================================
-- 7 REPORTES DE ERRORES
-- ============================================================
CREATE TABLE reportes_errores (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_traduccion INT NULL,
    tipo_traduccion ENUM('texto_a_senas','senas_a_texto'),
    descripcion_error TEXT NOT NULL,
    evidencia_url VARCHAR(255) NOT NULL,
    prioridad ENUM('baja', 'media', 'alta') DEFAULT 'media',
    estado ENUM('pendiente','en_revision') DEFAULT 'pendiente',
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario_reporta INT NULL,
    
    FOREIGN KEY (id_traduccion) REFERENCES traducciones(id_traduccion) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario_reporta) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 8 RENDIMIENTO DEL MODELO IA 
-- ============================================================
CREATE TABLE rendimiento_modelo (
    id_rendimiento INT AUTO_INCREMENT PRIMARY KEY,
    precision_actual DECIMAL(5,2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    id_administrador_actualizo INT NULL,
    
    FOREIGN KEY (id_administrador_actualizo) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ============================================================
-- 9 ESTADÍSTICAS (Vista dinámica)
-- ============================================================
CREATE OR REPLACE VIEW vista_estadisticas AS
SELECT
    (SELECT COUNT(*) FROM traducciones) AS total_traducciones,
    (SELECT COUNT(*) FROM contribuciones_senas) AS total_contribuciones,
    (SELECT COUNT(*) FROM contribuciones_senas WHERE estado = 'pendiente') AS contribuciones_pendientes,
    (SELECT COUNT(*) FROM contribuciones_senas WHERE estado = 'aprobada') AS contribuciones_aprobadas,
    (SELECT COUNT(*) FROM repositorio_senas_oficial) AS senas_oficiales,
    (SELECT COUNT(*) FROM reportes_errores) AS reportes_activos,
    (SELECT precision_actual FROM rendimiento_modelo ORDER BY ultima_actualizacion DESC LIMIT 1) AS precision_modelo,
    NOW() AS fecha_actualizacion;
-- ============================================================
-- 10 TOKENS DE RECUPERACIÓN
-- ============================================================
CREATE TABLE tokens_recuperacion (
    id_token INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE INDEX idx_tokens_expiracion ON tokens_recuperacion(fecha_expiracion);

-- ============================================================
-- 11 TRIGGERS: Obligación de asociación colaborador → administrador
-- ============================================================
DELIMITER //
CREATE TRIGGER trg_colaborador_requiere_admin
BEFORE INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.id_rol = 2 AND NEW.id_administrador_aprobo IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: todo colaborador debe estar asociado a un administrador que lo apruebe.';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_colaborador_requiere_admin_update
BEFORE UPDATE ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.id_rol = 2 AND NEW.id_administrador_aprobo IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: un colaborador no puede quedar sin administrador asociado.';
    END IF;
END;
//
DELIMITER ;
