// Navbar Component - Frontend
document.addEventListener('DOMContentLoaded', function () {
    initNavbar();
    setActiveNavLink();
    // updateAuthUI(); // Descomentar cuando tengas el sistema de autenticación
});

function setActiveNavLink() {
    const currentPath = window.location.pathname;
    
    // Desktop menu links
    const desktopLinks = document.querySelectorAll('.navbar-menu-item .navbar-link');
    desktopLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Mobile menu links
    const mobileLinks = document.querySelectorAll('.mobile-menu-link');
    mobileLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

function initNavbar() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobile = document.getElementById('closeMobile');
    const mobileOverlay = document.getElementById('mobileOverlay');

    // Hamburger menu toggle
    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', () => {
            mobileMenu.classList.add('open');
            if (mobileOverlay) {
                mobileOverlay.classList.add('active');
            }
            hamburger.setAttribute('aria-expanded', 'true');
            mobileMenu.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        });
    }

    // Close mobile menu
    if (closeMobile && mobileMenu) {
        closeMobile.addEventListener('click', () => {
            closeMobileMenu();
        });
    }

    // Overlay click
    if (mobileOverlay && mobileMenu) {
        mobileOverlay.addEventListener('click', () => {
            closeMobileMenu();
        });
    }

    function closeMobileMenu() {
        mobileMenu.classList.remove('open');
        if (mobileOverlay) {
            mobileOverlay.classList.remove('active');
        }
        if (hamburger) {
            hamburger.setAttribute('aria-expanded', 'false');
        }
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    // User dropdown toggle
    const userMenuBtn = document.getElementById('userMenuBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const chevronIcon = document.getElementById('chevronIcon');

    if (userMenuBtn && dropdownMenu) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = dropdownMenu.style.display === 'none';
            dropdownMenu.style.display = isHidden ? 'block' : 'none';

            if (chevronIcon) {
                chevronIcon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            if (dropdownMenu.style.display === 'block') {
                dropdownMenu.style.display = 'none';
                if (chevronIcon) {
                    chevronIcon.style.transform = 'rotate(0deg)';
                }
            }
        });
    }

    // Logout buttons
    const logoutBtn = document.getElementById('logoutBtn');
    const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogout();
        });
    }

    if (mobileLogoutBtn) {
        mobileLogoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogout();
        });
    }
}

// Logout function
function handleLogout() {
    if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
        // Redirigir a la ruta de logout en Flask
        window.location.href = '/logout';
    }
}

// Function to update auth UI (to be implemented with backend)
function updateAuthUI() {
    // Esta función se llamará cuando tengas el sistema de autenticación
    const isAuthenticated = false; // Cambiar por verificación real
    
    const loginBtn = document.getElementById('loginBtn');
    const userDropdown = document.getElementById('userDropdown');
    const mobileLoginBtn = document.getElementById('mobileLoginBtn');
    const mobileUserSection = document.getElementById('mobileUserSection');

    if (isAuthenticated) {
        // Mostrar dropdown de usuario
        if (loginBtn) loginBtn.style.display = 'none';
        if (userDropdown) userDropdown.style.display = 'block';
        if (mobileLoginBtn) mobileLoginBtn.style.display = 'none';
        if (mobileUserSection) mobileUserSection.style.display = 'flex';

        // Actualizar información del usuario
        const usuario = {
            nombre: 'Usuario Demo',
            email: 'usuario@ejemplo.com',
            avatar: null
        };

        updateUserInfo(usuario);
    } else {
        // Mostrar botones de login
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (userDropdown) userDropdown.style.display = 'none';
        if (mobileLoginBtn) mobileLoginBtn.style.display = 'block';
        if (mobileUserSection) mobileUserSection.style.display = 'none';
    }
}

// Update user information in navbar
function updateUserInfo(usuario) {
    // Desktop
    const userName = document.getElementById('userName');
    const dropdownUserName = document.getElementById('dropdownUserName');
    const dropdownUserEmail = document.getElementById('dropdownUserEmail');
    const userAvatar = document.getElementById('userAvatar');

    if (userName) userName.textContent = usuario.nombre;
    if (dropdownUserName) dropdownUserName.textContent = usuario.nombre;
    if (dropdownUserEmail) dropdownUserEmail.textContent = usuario.email;

    if (userAvatar && usuario.avatar) {
        userAvatar.innerHTML = `<img src="${usuario.avatar}" alt="${usuario.nombre}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
    } else if (userAvatar) {
        const iniciales = usuario.nombre.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
        userAvatar.innerHTML = iniciales;
    }

    // Mobile
    const mobileUserName = document.getElementById('mobileUserName');
    const mobileUserEmail = document.getElementById('mobileUserEmail');
    const mobileUserAvatar = document.getElementById('mobileUserAvatar');

    if (mobileUserName) mobileUserName.textContent = usuario.nombre;
    if (mobileUserEmail) mobileUserEmail.textContent = usuario.email;

    if (mobileUserAvatar && usuario.avatar) {
        mobileUserAvatar.innerHTML = `<img src="${usuario.avatar}" alt="${usuario.nombre}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
    } else if (mobileUserAvatar) {
        const iniciales = usuario.nombre.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
        mobileUserAvatar.innerHTML = iniciales;
    }
}

// Export functions for external use
window.NavbarAuth = {
    refresh: updateAuthUI,
    updateUser: updateUserInfo
};
