// Navegación simple entre secciones del perfil
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item:not(.logout)');
    const sections = document.querySelectorAll('.profile-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            
            // Remover clase activa de todos los elementos
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Agregar clase activa al elemento clickeado y su sección
            this.classList.add('active');
            const targetSection = document.getElementById(`section-${sectionId}`);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
    
    // Validación para eliminar cuenta
    const confirmInput = document.getElementById('confirm-delete');
    const deleteBtn = document.getElementById('delete-btn');
    
    if (confirmInput && deleteBtn) {
        confirmInput.addEventListener('input', function() {
            if (this.value.toUpperCase() === 'ELIMINAR') {
                deleteBtn.disabled = false;
                deleteBtn.classList.add('enabled');
            } else {
                deleteBtn.disabled = true;
                deleteBtn.classList.remove('enabled');
            }
        });
    }
});

// Función para cerrar sesión
function logout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        // Redirigir a la ruta de logout de auth
        window.location.href = '/auth/logout';
    }
}