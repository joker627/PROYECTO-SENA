// Navbar behaviors: hamburger, user dropdown, notifications
document.addEventListener('DOMContentLoaded', function() {
    initHamburgerMenu();
    initUserDropdown();
    // updateNotificationBadge handled globally in update-badge.js
});

// Hamburger menu
function initHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const closeMenu = document.querySelector('.close-menu');
    const overlay = document.querySelector('.overlay');

    if (!hamburger || !mobileMenu) return;

    // Open mobile menu
    hamburger.addEventListener('click', () => {
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Close mobile menu
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

    // Close on link click
    document.querySelectorAll('.mobile-menu a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeMobileMenu();
        }
    });
}

// User dropdown (desktop)
function initUserDropdown() {
    const userSection = document.querySelector('.user-section');
    const userDropdownTrigger = document.querySelector('.user-dropdown-trigger');

    if (!userDropdownTrigger || !userSection) return;

    // Accessibility: set ARIA attributes
    try {
        userDropdownTrigger.setAttribute('aria-haspopup', 'true');
        if (!userDropdownTrigger.hasAttribute('aria-expanded')) {
            userDropdownTrigger.setAttribute('aria-expanded', 'false');
        }
    } catch (err) {}

    // Toggle user dropdown
    userDropdownTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        // Cerrar notificaciones si está abierto
        userSection.classList.remove('notifications-active');
        // Toggle dropdown de usuario
        const opening = !userSection.classList.contains('active');
        userSection.classList.toggle('active');
        // update aria-expanded
        try { userDropdownTrigger.setAttribute('aria-expanded', opening ? 'true' : 'false'); } catch (err) {}
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (!userSection.contains(e.target)) {
            userSection.classList.remove('active');
            userSection.classList.remove('notifications-active');
            try { userDropdownTrigger.setAttribute('aria-expanded', 'false'); } catch (err) {}
        }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            userSection.classList.remove('active');
            userSection.classList.remove('notifications-active');
            try { userDropdownTrigger.setAttribute('aria-expanded', 'false'); } catch (err) {}
        }
    });
}

// Notifications (desktop)
// Notification UI removed: no desktop/mobile notification init functions remain.

// Update notification badge (single-call helper)
async function updateNotificationBadge() {
    // Stub: notifications removed. No-op to avoid fetch errors.
    console.debug('updateNotificationBadge(): stubbed because notifications were removed');
}
