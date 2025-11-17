-- ============================================================
-- 📦 DATOS DE EJEMPLO PARA SIGN_TECHNOLOGY
-- ============================================================

USE sign_technology;

-- ============================================================
-- 1️⃣ USUARIOS
-- ============================================================
INSERT INTO usuarios (nombre_completo, correo, contrasena, id_rol, estado, id_administrador_aprobo) VALUES
-- Administradores
('Admin Principal', 'admin@signtech.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/2oHlCFD5RKzYcW5Su', 1, 'activo', NULL),
('Ana García López', 'ana.garcia@admin.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/2oHlCFD5RKzYcW5Su', 1, 'activo', NULL),

-- Colaboradores (aprobados por admin)
('Carlos Rodríguez', 'carlos.rodriguez@colab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/2oHlCFD5RKzYcW5Su', 2, 'activo', 1),
('María Fernández', 'maria.fernandez@colab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/2oHlCFD5RKzYcW5Su', 2, 'activo', 1),
('Pedro Martínez', 'pedro.martinez@colab.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/2oHlCFD5RKzYcW5Su', 2, 'inactivo', 2);

-- ============================================================
-- 2️⃣ SOLICITUDES COLABORADOR
-- ============================================================
INSERT INTO solicitudes_colaborador (
    nombre_completo, correo, telefono, tipo_documento, numero_documento, 
    archivo_identidad, descripcion, acepto_terminos, estado, id_administrador_reviso, fecha_revision
) VALUES
-- Solicitud aprobada
('Laura Méndez', 'laura.mendez@solicitud.com', '+573001234567', 'cedula', '1234567890', 
 '/docs/cedula_laura.jpg', 'Intérprete con 3 años de experiencia en LSC', TRUE, 'aprobada', 1, NOW()),

-- Solicitud pendiente
('Javier Ruiz', 'javier.ruiz@solicitud.com', '+573002345678', 'dni', '987654321', 
 '/docs/dni_javier.jpg', 'Educador especializado en lengua de señas', TRUE, 'pendiente', NULL, NULL),

-- Solicitud rechazada
('Sofía Castro', 'sofia.castro@solicitud.com', '+573003456789', 'pasaporte', 'AB123456', 
 '/docs/pasaporte_sofia.jpg', 'Estudiante de lingüística', TRUE, 'rechazada', 2, NOW());

-- ============================================================
-- 3️⃣ USUARIOS ANÓNIMOS
-- ============================================================
INSERT INTO usuarios_anonimos (uuid_visitante) VALUES
(UUID()), (UUID()), (UUID()), (UUID()), (UUID());

-- ============================================================
-- 4️⃣ CONTRIBUCIONES DE SEÑAS
-- ============================================================
INSERT INTO contribuciones_senas (
    palabra_asociada, descripcion, archivo_video, id_usuario_gestiono, estado, 
    fecha_gestion, fecha_repositorio, observaciones_gestion
) VALUES
-- Contribución en repositorio (aprobada por admin)
('hola', 'Saludo inicial estándar', '/videos/senas/hola_estandar.mp4', 1, 'en_repositorio', 
 NOW(), NOW(), 'Seña básica aprobada'),

-- Contribución en repositorio (aprobada por colaborador)
('gracias', 'Expresión de agradecimiento', '/videos/senas/gracias_estandar.mp4', 3, 'en_repositorio', 
 NOW(), NOW(), 'Seña correcta y clara'),

-- Contribución aprobada pero no en repositorio aún
('por favor', 'Solicitud educada', '/videos/senas/por_favor.mp4', 4, 'aprobada', 
 NOW(), NULL, 'Buena ejecución'),

-- Contribución pendiente
('ayuda', 'Solicitud de asistencia', '/videos/senas/ayuda_pendiente.mp4', NULL, 'pendiente', 
 NULL, NULL, NULL),

-- Contribución rechazada
('adiós', 'Despedida informal', '/videos/senas/adios_rechazado.mp4', 2, 'rechazada', 
 NOW(), NULL, 'Seña no estándar, usar versión formal');

-- ============================================================
-- 5️⃣ REPOSITORIO OFICIAL DE SEÑAS
-- ============================================================
INSERT INTO repositorio_senas_oficial (
    palabra_asociada, archivo_video, id_contribucion_origen, id_usuario_valido
) VALUES
('hola', '/videos/senas/hola_estandar.mp4', 1, 1),
('gracias', '/videos/senas/gracias_estandar.mp4', 2, 3),
('familia', '/videos/senas/familia_oficial.mp4', 3, 1),
('amigo', '/videos/senas/amigo_oficial.mp4', 4, 2);

-- ============================================================
-- 6️⃣ TRADUCCIONES
-- ============================================================
INSERT INTO traducciones (
    tipo_traduccion, texto_entrada, enlace_sena_entrada, resultado_salida, fallo, id_usuario, id_anonimo
) VALUES
-- Traducciones exitosas
('texto_a_senas', 'Hola amigos', NULL, 'Seña: Hola + Amigos', FALSE, 3, NULL),
('senas_a_texto', NULL, '/videos/entrada/usuario1.mp4', 'Quiero aprender', FALSE, NULL, 1),
('texto_a_senas', 'Gracias por la ayuda', NULL, 'Seña: Gracias + ayuda', FALSE, 4, NULL),

-- Traducciones con fallo
('texto_a_senas', 'Buenos días a todos', NULL, 'Error: No se encontró seña para "todos"', TRUE, NULL, 2),
('senas_a_texto', NULL, '/videos/entrada/usuario2.mp4', 'Error en reconocimiento de seña rápida', TRUE, 5, NULL),

-- Traducciones anónimas exitosas
('texto_a_senas', '¿Dónde está el baño?', NULL, 'Seña: ¿Dónde? + baño', FALSE, NULL, 3),
('senas_a_texto', NULL, '/videos/entrada/usuario3.mp4', 'Me llamo María', FALSE, NULL, 4);

-- ============================================================
-- 7️⃣ REPORTES DE ERRORES
-- ============================================================
INSERT INTO reportes_errores (
    id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, id_usuario_reporta
) VALUES
(4, 'texto_a_senas', 'La seña para "todos" existe pero no se reconoce', '/evidencias/error_todos.jpg', 'alta', 'pendiente', 3),
(5, 'senas_a_texto', 'Confunde seña "hola" con "adiós" en movimientos rápidos', '/evidencias/error_hola_adios.mp4', 'media', 'en_revision', 4),
(NULL, 'texto_a_senas', 'Error general en frases con múltiples palabras', '/evidencias/error_frases.jpg', 'alta', 'pendiente', 1);

-- ============================================================
-- 8️⃣ RENDIMIENTO DEL MODELO IA
-- ============================================================
INSERT INTO rendimiento_modelo (
    precision_actual, observaciones, id_administrador_actualizo
) VALUES
(82.50, 'Modelo inicial con dataset básico', 1),
(85.75, 'Mejora tras añadir 50 señas validadas', 1),
(88.20, 'Optimización del algoritmo de reconocimiento', 2),
(90.50, 'Máximo histórico con nuevo dataset', 1);

-- ============================================================
-- 9️⃣ TOKENS DE RECUPERACIÓN
-- ============================================================
INSERT INTO tokens_recuperacion (
    id_usuario, token, fecha_expiracion, usado
) VALUES
(3, 'token_carlos_recuperacion', DATE_ADD(NOW(), INTERVAL 1 HOUR), FALSE),
(4, 'token_maria_recuperacion', DATE_SUB(NOW(), INTERVAL 2 HOUR), FALSE);

-- ============================================================
-- 📊 CONSULTAS DE VERIFICACIÓN
-- ============================================================

-- Verificar conteo de datos
SELECT 'Usuarios' as tabla, COUNT(*) as total FROM usuarios
UNION ALL SELECT 'Solicitudes Colaborador', COUNT(*) FROM solicitudes_colaborador
UNION ALL SELECT 'Contribuciones', COUNT(*) FROM contribuciones_senas
UNION ALL SELECT 'Repositorio Oficial', COUNT(*) FROM repositorio_senas_oficial
UNION ALL SELECT 'Traducciones', COUNT(*) FROM traducciones
UNION ALL SELECT 'Reportes Error', COUNT(*) FROM reportes_errores;

-- Ver estadísticas actuales
SELECT * FROM vista_estadisticas;

-- Contribuciones por estado
SELECT estado, COUNT(*) as cantidad 
FROM contribuciones_senas 
GROUP BY estado;

-- Traducciones por tipo y resultado
SELECT 
    tipo_traduccion,
    COUNT(*) as total,
    SUM(fallo) as errores,
    ROUND((SUM(fallo) * 100.0 / COUNT(*)), 2) as tasa_error
FROM traducciones 
GROUP BY tipo_traduccion;