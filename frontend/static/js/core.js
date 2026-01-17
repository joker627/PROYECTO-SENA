/**
 * Sign Technology - Core JavaScript (Optimizado)
 * Consolida: main.js, menu.js, layout.js
 * Versión: 2.0 - Optimizado para rendimiento
 */

(function() {
    'use strict';

    // ═══════════════════════════════════════════════════════════
    // CONFIGURACIÓN Y CACHE DE ELEMENTOS
    // ═══════════════════════════════════════════════════════════
    
    const cache = {};
    
    const $ = (selector, parent = document) => {
        const key = selector + (parent === document ? '' : parent.id);
        return cache[key] || (cache[key] = parent.querySelector(selector));
    };
    
    const $$ = (selector, parent = document) => parent.querySelectorAll(selector);

    // ═══════════════════════════════════════════════════════════
    // NAVBAR - Menú móvil y dropdown de usuario
    // ═══════════════════════════════════════════════════════════
    
    function initNavbar() {
        const hamburger = $('#hamburger');
        const mobileMenu = $('#mobileMenu');
        const closeMobile = $('#closeMobile');
        const mobileOverlay = $('#mobileOverlay');
        const userMenuBtn = $('#userMenuBtn');
        const dropdownMenu = $('#dropdownMenu');

        // Toggle menú móvil
        if (hamburger && mobileMenu) {
            hamburger.onclick = () => toggleMobileMenu(true);
        }
        
        if (closeMobile) {
            closeMobile.onclick = () => toggleMobileMenu(false);
        }
        
        if (mobileOverlay) {
            mobileOverlay.onclick = () => toggleMobileMenu(false);
        }

        function toggleMobileMenu(open) {
            if (!mobileMenu) return;
            mobileMenu.classList.toggle('open', open);
            mobileOverlay?.classList.toggle('active', open);
            document.body.style.overflow = open ? 'hidden' : '';
            hamburger?.setAttribute('aria-expanded', open);
        }

        // Dropdown de usuario
        if (userMenuBtn && dropdownMenu) {
            userMenuBtn.onclick = (e) => {
                e.stopPropagation();
                const isOpen = dropdownMenu.style.display === 'block';
                dropdownMenu.style.display = isOpen ? 'none' : 'block';
                const chevron = $('#chevronIcon');
                if (chevron) chevron.style.transform = isOpen ? '' : 'rotate(180deg)';
            };

            document.onclick = () => {
                if (dropdownMenu.style.display === 'block') {
                    dropdownMenu.style.display = 'none';
                    const chevron = $('#chevronIcon');
                    if (chevron) chevron.style.transform = '';
                }
            };
        }
    }

    // ═══════════════════════════════════════════════════════════
    // SIDEBAR - Panel lateral admin
    // ═══════════════════════════════════════════════════════════
    
    function initSidebar() {
        const mobileMenuBtn = $('#mobileMenuBtn');
        const sidebar = $('.sidebar');
        const overlay = $('#overlay');
        const collapseBtn = $('#sidebarCollapseBtn');

        if (!sidebar) return;

        // Toggle móvil
        if (mobileMenuBtn && overlay) {
            mobileMenuBtn.onclick = () => toggleSidebar(true);
            overlay.onclick = () => toggleSidebar(false);
        }

        function toggleSidebar(open) {
            sidebar.classList.toggle('open', open);
            overlay?.classList.toggle('active', open);
        }

        // Colapsar en desktop
        if (collapseBtn) {
            collapseBtn.onclick = () => {
                sidebar.classList.toggle('collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            };

            // Restaurar estado
            if (localStorage.getItem('sidebarCollapsed') === 'true') {
                sidebar.classList.add('collapsed');
            }
        }

        // Cerrar en resize a desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1024) toggleSidebar(false);
        }, { passive: true });
    }

    // ═══════════════════════════════════════════════════════════
    // NAVEGACIÓN ACTIVA
    // ═══════════════════════════════════════════════════════════
    
    function setActiveLinks() {
        const path = window.location.pathname;
        $$('.navbar-link, .mobile-menu-link, .nav-link').forEach(link => {
            const href = link.getAttribute('href');
            link.classList.toggle('active', href === path);
        });
    }

    // ═══════════════════════════════════════════════════════════
    // UTILIDADES GLOBALES
    // ═══════════════════════════════════════════════════════════
    
    window.SignTech = {
        // Formato de fecha
        formatDate: (date) => new Date(date).toLocaleDateString('es-CO', {
            day: '2-digit', month: '2-digit', year: 'numeric'
        }),
        
        // Formato fecha con hora
        formatDateTime: (date) => new Date(date).toLocaleString('es-CO', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        }),

        // Cerrar modal genérico
        closeModal: (id) => {
            const modal = document.getElementById(id);
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
                // Pausar videos
                const video = modal.querySelector('video');
                if (video) { video.pause(); video.src = ''; }
            }
        },

        // Abrir modal genérico
        openModal: (id) => {
            const modal = document.getElementById(id);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }
    };

    // ═══════════════════════════════════════════════════════════
    // ESCAPE PARA CERRAR MODALES
    // ═══════════════════════════════════════════════════════════
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            $$('.modal.active').forEach(m => SignTech.closeModal(m.id));
        }
    });

    // ═══════════════════════════════════════════════════════════
    // INICIALIZACIÓN
    // ═══════════════════════════════════════════════════════════
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        initNavbar();
        initSidebar();
        setActiveLinks();
    }

})();
