// Menú: toggle y gestión accesible
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.nav-hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    // Alterna el menú y actualiza atributos ARIA
    function toggleMenu() {
        const willOpen = !navLinks.classList.contains('active');
        if (willOpen) {
            hamburger.classList.add('active');
            navLinks.classList.add('active');
            navLinks.setAttribute('aria-hidden', 'false');
            hamburger.setAttribute('aria-expanded', 'true');
        } else {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
            navLinks.setAttribute('aria-hidden', 'true');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    }
    
    // Abrir/cerrar menú al hacer clic en el ícono
    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleMenu();
        const expanded = hamburger.classList.contains('active');
        hamburger.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    });
    
    // Cerrar menú al hacer clic en un enlace
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                toggleMenu();
            }
        });
    });

    // Cerrar menú al hacer clic fuera de él
    document.addEventListener('click', function(e) {
        const isClickInsideMenu = navLinks.contains(e.target) || hamburger.contains(e.target);
        if (!isClickInsideMenu && navLinks.classList.contains('active')) {
            toggleMenu();
        }
    });
    
    // Cerrar menú al desplazarse
    window.addEventListener('scroll', function() {
        if (navLinks.classList.contains('active')) {
            toggleMenu();
        }
    });
    // Ocultar notificaciones flash automáticamente
    setTimeout(function() {
        document.querySelectorAll('.flash-message').forEach(function(msg) {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(function() { msg.remove(); }, 500);
        });
    }, 4000);

    // Menú desplegable de usuario (ajustes/perfil)
    const dropdown = document.querySelector('.nav-dropdown');
    const dropdownToggle = document.querySelector('.nav-dropdown-toggle');
    if (dropdown && dropdownToggle) {
        dropdownToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('open');
            const expanded = dropdown.classList.contains('open');
            dropdownToggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        });

        // Cerrar el dropdown al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
                dropdownToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }


});
