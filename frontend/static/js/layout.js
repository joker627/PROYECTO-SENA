/* Layout JavaScript - Sidebar & Mobile Menu */

document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('overlay');

    if (mobileMenuBtn && sidebar && overlay) {
        // Toggle Sidebar
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        });

        // Close Sidebar when clicking overlay
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });

        // Close sidebar on window resize to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1024) {
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            }
        });
        // Desktop Collapse Toggle
        const sidebarCollapseBtn = document.getElementById('sidebarCollapseBtn');
        if (sidebarCollapseBtn) {
            sidebarCollapseBtn.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
                // Optional: Save preference to localStorage
                const isCollapsed = sidebar.classList.contains('collapsed');
                localStorage.setItem('sidebarCollapsed', isCollapsed);
            });

            // Restore state
            if (localStorage.getItem('sidebarCollapsed') === 'true') {
                sidebar.classList.add('collapsed');
            }
        }
    }

    // User menu dropdown
    const userCardBtn = document.querySelector('.user-card-btn');
    const userDropdown = document.getElementById('userDropdown');

    if (userCardBtn && userDropdown) {
        userCardBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userCardBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // Password visibility toggles
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const targetId = toggle.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = toggle.querySelector('img');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.src = icon.src.replace('visibility.svg', 'visibility-off.svg');
            } else {
                input.type = 'password';
                icon.src = icon.src.replace('visibility-off.svg', 'visibility.svg');
            }
        });
    });
});
