
// Crear contenedor de toasts si no existe
function initToastContainer() {
    if (!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
}

// Mostrar un toast mínimo con opciones básicas 
function showToast(message, type = 'info', duration = 5000) {
    initToastContainer();
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: '<i class="fas fa-check-circle"></i>',
        error: '<i class="fas fa-times-circle"></i>',
        warning: '<i class="fas fa-exclamation-triangle"></i>',
        info: '<i class="fas fa-info-circle"></i>'
    };

    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-content">
            <p class="toast-message">${message}</p>
        </div>
        <button class="toast-close"><i class="fas fa-times"></i></button>
        ${duration > 0 ? '<div class="toast-progress"></div>' : ''}
    `;

    container.appendChild(toast);

    const closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) closeBtn.addEventListener('click', () => closeToast(closeBtn));

    if (duration > 0) {
        setTimeout(() => {
            if (closeBtn) closeToast(closeBtn);
            else closeToast(toast);
        }, duration);
    }

    return toast;
}

// Cerrar un toast específico
function closeToast(target) {
    if (!target) return;
    let toast = null;
    if (target.classList && target.classList.contains('toast')) {
        toast = target;
    } else if (typeof target.closest === 'function') {
        toast = target.closest('.toast');
    }
    
    // Si se encuentra el toast, iniciar animación de cierre y eliminarlo
    if (toast) {
        toast.classList.add('toast-hiding');
        setTimeout(() => {
            toast.remove();
            const container = document.getElementById('toast-container');
            if (container && container.children.length === 0) container.remove();
        }, 300);
    }
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

            // Limpiar texto de la X de cierre si existe
            const message = alert.textContent.replace('fa-solid fa-xmark').trim();
            showToast(message, type);
        });

        // Ocultar flash messages originales
        flashMessages.style.display = 'none';
    }
});
