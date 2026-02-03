// Main JavaScript - Frontend
// Este archivo se carga en todas las páginas

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    console.log('Frontend inicializado');
    
    // Resaltar link activo en navegación
    highlightActiveLink();
});

// Función para resaltar el link activo según la URL actual
function highlightActiveLink() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.navbar-link, .mobile-menu-link');
    
    links.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        if (currentPath === linkPath) {
            link.classList.add('active');
        }
    });
}

// Utilidades globales
window.utils = {
    // Formato de moneda
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0
        }).format(amount);
    },
    
    // Formato de fecha
    formatDate: function(date) {
        return new Intl.DateTimeFormat('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Mostrar mensaje de notificación (toast)
    showToast: function(message, type = 'info') {
        // Implementar sistema de notificaciones toast
        console.log(`[${type.toUpperCase()}]: ${message}`);
    }
};
