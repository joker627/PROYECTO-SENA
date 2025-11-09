// Sistema global de notificaciones toast

// Cache para prevenir toasts duplicados
const toastCache = new Map();
const TOAST_CACHE_DURATION = 3000; // 3 segundos para considerar un toast como duplicado

// Crear contenedor de toasts si no existe
function initToastContainer() {
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
}

// Generar hash único para un toast
function getToastHash(message, type, title) {
    return `${type}-${title}-${message}`;
}

// Verificar si el toast es duplicado
function isDuplicateToast(message, type, title) {
    const hash = getToastHash(message, type, title);
    const now = Date.now();
    
    if (toastCache.has(hash)) {
        const lastShown = toastCache.get(hash);
        if (now - lastShown < TOAST_CACHE_DURATION) {
            console.log('🚫 Toast duplicado bloqueado:', message);
            return true;
        }
    }
    
    toastCache.set(hash, now);
    
    // Limpiar cache antiguo
    setTimeout(() => {
        toastCache.delete(hash);
    }, TOAST_CACHE_DURATION);
    
    return false;
}

// Mostrar toast
function showToast(message, type = 'info', title = null, duration = 5000) {
    // Títulos por defecto
    const defaultTitles = {
        success: 'Éxito',
        error: 'Error',
        warning: 'Advertencia',
        info: 'Información'
    };
    
    const toastTitle = title || defaultTitles[type] || defaultTitles.info;
    
    // PREVENIR DUPLICADOS
    if (isDuplicateToast(message, type, toastTitle)) {
        return null; // No mostrar toast duplicado
    }
    
    initToastContainer();
    
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Iconos según tipo
    const icons = {
        success: '<i class="fas fa-check-circle"></i>',
        error: '<i class="fas fa-times-circle"></i>',
        warning: '<i class="fas fa-exclamation-triangle"></i>',
        info: '<i class="fas fa-info-circle"></i>'
    };
    
    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-content">
            <p class="toast-title">${toastTitle}</p>
            <p class="toast-message">${message}</p>
        </div>
        <button class="toast-close" onclick="closeToast(this)">
            <i class="fas fa-times"></i>
        </button>
        ${duration > 0 ? '<div class="toast-progress"></div>' : ''}
    `;
    
    container.appendChild(toast);
    
    // Auto-cerrar después del tiempo especificado
    if (duration > 0) {
        setTimeout(() => {
            closeToast(toast.querySelector('.toast-close'));
        }, duration);
    }
    
    return toast;
}

// Cerrar toast
function closeToast(button) {
    const toast = button.closest('.toast');
    if (toast) {
        toast.classList.add('toast-hiding');
        setTimeout(() => {
            toast.remove();
            
            // Limpiar contenedor si está vacío
            const container = document.getElementById('toast-container');
            if (container && container.children.length === 0) {
                container.remove();
            }
        }, 300);
    }
}

// Funciones de acceso rápido
function toastSuccess(message, title = null, duration = 5000) {
    return showToast(message, 'success', title, duration);
}

function toastError(message, title = null, duration = 5000) {
    return showToast(message, 'error', title, duration);
}

function toastWarning(message, title = null, duration = 5000) {
    return showToast(message, 'warning', title, duration);
}

function toastInfo(message, title = null, duration = 5000) {
    return showToast(message, 'info', title, duration);
}

// Convertir flash messages a toasts al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        const alerts = flashMessages.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const classList = Array.from(alert.classList);
            let type = 'info';
            
            if (classList.includes('alert-success')) type = 'success';
            else if (classList.includes('alert-error') || classList.includes('alert-danger')) type = 'error';
            else if (classList.includes('alert-warning')) type = 'warning';
            
            const message = alert.textContent.replace('×', '').trim();
            showToast(message, type);
        });
        
        // Ocultar flash messages originales
        flashMessages.style.display = 'none';
    }
});
