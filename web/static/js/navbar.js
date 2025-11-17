// NAVBAR - Menú hamburguesa, Dropdown usuario, Notificaciones

document.addEventListener('DOMContentLoaded', function() {
    initHamburgerMenu();
    initUserDropdown();
    
});

// ========== MENÚ HAMBURGUESA ==========
function initHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const closeMenu = document.querySelector('.close-menu');
    const overlay = document.querySelector('.overlay');

    if (!hamburger || !mobileMenu) return;

    // Abrir menú móvil
    hamburger.addEventListener('click', () => {
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Cerrar menú móvil
    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    if (closeMenu) {
        closeMenu.addEventListener('click', closeMobileMenu);
    }

    if (overlay) {
        overlay.addEventListener('click', closeMobileMenu);
    }

    // Cerrar menú al hacer clic en un enlace
    document.querySelectorAll('.mobile-menu a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Cerrar menú con tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeMobileMenu();
        }
    });
}

// ========== DROPDOWN DE USUARIO (Desktop) ==========
function initUserDropdown() {
    const userSection = document.querySelector('.user-section');
    const userDropdownTrigger = document.querySelector('.user-dropdown-trigger');

    if (!userDropdownTrigger || !userSection) return;

    // Toggle dropdown al hacer clic en el avatar
    userDropdownTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        // Cerrar notificaciones si está abierto
        userSection.classList.remove('notifications-active');
        // Toggle dropdown de usuario
        userSection.classList.toggle('active');
    });

    // Cerrar dropdown al hacer clic fuera
    document.addEventListener('click', (e) => {
        if (!userSection.contains(e.target)) {
            userSection.classList.remove('active');
            userSection.classList.remove('notifications-active');
        }
    });

    // Cerrar dropdown con tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            userSection.classList.remove('active');
            userSection.classList.remove('notifications-active');
        }
    });
}