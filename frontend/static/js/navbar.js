// ===========================
// NAVBAR - Menú hamburguesa, Dropdown usuario, Notificaciones
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    initHamburgerMenu();
    initUserDropdown();
    initNotifications();
    initMobileNotifications();
    
    // NO ejecutar updateNotificationBadge aquí - lo hace update-badge.js globalmente
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

// ========== NOTIFICACIONES (Desktop) ==========
function initNotifications() {
    const userSection = document.querySelector('.user-section');
    const notificationsBtn = document.querySelector('.notifications-btn');

    if (!notificationsBtn || !userSection) return;

    // Toggle notificaciones al hacer clic en la campana
    notificationsBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        // Cerrar dropdown de usuario si está abierto
        userSection.classList.remove('active');
        // Toggle dropdown de notificaciones
        userSection.classList.toggle('notifications-active');
    });
}

// ========== NOTIFICACIONES MÓVILES ==========
function initMobileNotifications() {
    const mobileNotificationsBtn = document.querySelector('.mobile-notifications-btn');
    const mobileNotificationsPanel = document.querySelector('.mobile-notifications-panel');
    const closeNotificationsMobile = document.querySelector('.close-notifications-mobile');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.overlay');

    if (!mobileNotificationsBtn || !mobileNotificationsPanel) return;

    // Abrir panel de notificaciones móvil
    mobileNotificationsBtn.addEventListener('click', () => {
        mobileNotificationsPanel.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Cerrar panel de notificaciones móvil
    if (closeNotificationsMobile) {
        closeNotificationsMobile.addEventListener('click', () => {
            mobileNotificationsPanel.classList.remove('active');
            // Cerrar menú móvil también
            if (mobileMenu) {
                mobileMenu.classList.remove('active');
            }
            if (overlay) {
                overlay.classList.remove('active');
            }
            document.body.style.overflow = 'auto';
        });
    }

    // Cerrar con tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNotificationsPanel.classList.contains('active')) {
            mobileNotificationsPanel.classList.remove('active');
            if (mobileMenu) {
                mobileMenu.classList.remove('active');
            }
            if (overlay) {
                overlay.classList.remove('active');
            }
            document.body.style.overflow = 'auto';
        }
    });
}

// ========== ACTUALIZAR BADGE DE NOTIFICACIONES ==========
async function updateNotificationBadge() {
    try {
        const response = await fetch('/notifications/count');
        const data = await response.json();
        
        if (data.success) {
            const count = data.count;
            
            // Actualizar badge en desktop (navbar) - usa .notification-badge
            const desktopBadge = document.querySelector('.notifications-btn .notification-badge');
            if (desktopBadge) {
                desktopBadge.textContent = count;
                desktopBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // Actualizar badge en móvil (navbar) - usa .mobile-notification-badge
            const mobileBadge = document.querySelector('.mobile-notifications-btn .mobile-notification-badge');
            if (mobileBadge) {
                mobileBadge.textContent = count;
                mobileBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // Actualizar badge en el slider (dashboard) - usa .menu-badge
            const sliderBadge = document.querySelector('.sidebar .menu-item a[href*="notifications"] .menu-badge');
            if (sliderBadge) {
                sliderBadge.textContent = count;
                sliderBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // Actualizar badge específico del slider por ID
            const sliderBadgeById = document.getElementById('sliderNotificationBadge');
            if (sliderBadgeById) {
                sliderBadgeById.textContent = count;
                sliderBadgeById.style.display = count > 0 ? 'inline-flex' : 'none';
            }
            
            console.log(`[NAVBAR] Badge actualizado: ${count} notificaciones`);
        }
    } catch (error) {
        console.error('Error al actualizar badge de notificaciones:', error);
    }
}
