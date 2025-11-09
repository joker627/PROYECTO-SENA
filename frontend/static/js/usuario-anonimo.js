// Sistema de gestión de usuarios anónimos

// Registrar usuario anónimo automáticamente al cargar la página
async function registrarUsuarioAnonimo() {
    try {
        // Verificar si ya existe una sesión anónima
        const sesionResponse = await fetch('/api/anonimo/sesion');
        const sesionData = await sesionResponse.json();
        
        if (sesionData.success && sesionData.tiene_sesion) {
            console.log('[ANÓNIMO] Sesión existente:', sesionData.uuid_transaccion);
            return {
                success: true,
                uuid: sesionData.uuid_transaccion,
                id: sesionData.id_anonimo
            };
        }
        
        // Si no existe, crear nuevo usuario anónimo
        const response = await fetch('/api/anonimo/registrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('[ANÓNIMO] Nuevo usuario registrado:', data.uuid_transaccion);
            
            // Guardar en localStorage para persistencia
            localStorage.setItem('uuid_anonimo', data.uuid_transaccion);
            localStorage.setItem('id_anonimo', data.id_anonimo);
            
            return {
                success: true,
                uuid: data.uuid_transaccion,
                id: data.id_anonimo
            };
        } else {
            console.error('[ANÓNIMO] Error al registrar:', data.error);
            return {
                success: false,
                error: data.error
            };
        }
        
    } catch (error) {
        console.error('[ANÓNIMO] Error de red:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Obtener UUID del usuario anónimo actual
function obtenerUUIDanonimo() {
    return localStorage.getItem('uuid_anonimo');
}

// Obtener ID del usuario anónimo actual
function obtenerIdAnonimo() {
    return localStorage.getItem('id_anonimo');
}

// Validar si el UUID es válido
async function validarUsuarioAnonimo(uuid) {
    try {
        const response = await fetch(`/api/anonimo/validar/${uuid}`);
        const data = await response.json();
        
        return data.valido;
    } catch (error) {
        console.error('[ANÓNIMO] Error al validar:', error);
        return false;
    }
}

// Inicializar usuario anónimo al cargar cualquier página pública
document.addEventListener('DOMContentLoaded', async function() {
    // Solo registrar en páginas públicas (no en admin)
    const esAdmin = window.location.pathname.includes('/admin') || 
                    window.location.pathname.includes('/login');
    
    if (!esAdmin) {
        const resultado = await registrarUsuarioAnonimo();
        
        if (resultado.success) {
            console.log('[ANÓNIMO] Sistema inicializado correctamente');
            
            // Disparar evento personalizado para que otras funciones lo usen
            window.dispatchEvent(new CustomEvent('usuario-anonimo-listo', {
                detail: {
                    uuid: resultado.uuid,
                    id: resultado.id
                }
            }));
        }
    }
});

// Exportar funciones para uso global
window.usuarioAnonimo = {
    registrar: registrarUsuarioAnonimo,
    obtenerUUID: obtenerUUIDanonimo,
    obtenerId: obtenerIdAnonimo,
    validar: validarUsuarioAnonimo
};
