document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.nav-hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // Función para alternar el menú
    function toggleMenu() {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    }
    
    // Evento para el botón hamburguesa
    hamburger.addEventListener('click', function(e) {
        e.stopPropagation(); // Evita que el evento se propague al documento
        toggleMenu();
    });
    
    // Cerrar el menú al hacer clic en un enlace
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                toggleMenu();
            }
        });
    });
    
    // Cerrar el menú al hacer clic en cualquier parte fuera de él
    document.addEventListener('click', function(e) {
        const isClickInsideMenu = navLinks.contains(e.target) || hamburger.contains(e.target);
        
        if (!isClickInsideMenu && navLinks.classList.contains('active')) {
            toggleMenu();
        }
    });
    
    // Cerrar el menú al desplazarse (opcional)
    window.addEventListener('scroll', function() {
        if (navLinks.classList.contains('active')) {
            toggleMenu();
        }
    });
});