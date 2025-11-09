// Notificaciones - UI: alertas y confirmaciones

document.addEventListener('DOMContentLoaded', function() {
    initAutoCloseAlerts();
    initConfirmDialogs();
});

// Auto-cerrar alertas después de 5 segundos
function initAutoCloseAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Confirmaciones en formularios
function initConfirmDialogs() {
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Funciones globales de confirmación
function confirmDelete(message = '¿Estás seguro de eliminar esto?') {
    return confirm(message);
}

function confirmAction(message) {
    return confirm(message);
}
