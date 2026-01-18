/**
 * Sign Technology - Core JavaScript
 * Sistema de gestión frontend para traducción LSC
 */
(function() {
    'use strict';

    const $ = s => document.querySelector(s);
    const $$ = s => document.querySelectorAll(s);
    const $id = id => document.getElementById(id);

    /** Sistema global SignTech */
    window.SignTech = {
        formatDate: d => {
            if (!d || d === 'None') return '-';
            try { return new Date(d).toLocaleString('es-CO', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }); }
            catch { return d; }
        },
        openModal: id => {
            const m = $id(id);
            if (m) { m.classList.add('active'); document.body.style.overflow = 'hidden'; }
        },
        closeModal: id => {
            const m = $id(id);
            if (m) {
                m.classList.remove('active');
                document.body.style.overflow = '';
                const v = m.querySelector('video');
                if (v) { v.pause(); v.src = ''; }
            }
        }
    };

    window.closeModal = SignTech.closeModal;

    /** Navbar - Menú público */
    function initNavbar() {
        const hamburger = $id('hamburger');
        const mobileMenu = $id('mobileMenu');
        const closeMobile = $id('closeMobile');
        const mobileOverlay = $id('mobileOverlay');
        const userMenuBtn = $id('userMenuBtn');
        const dropdownMenu = $id('dropdownMenu');

        function toggleMobile(open) {
            if (!mobileMenu) return;
            mobileMenu.classList.toggle('open', open);
            mobileOverlay?.classList.toggle('active', open);
            document.body.style.overflow = open ? 'hidden' : '';
        }

        if (hamburger) hamburger.onclick = () => toggleMobile(true);
        if (closeMobile) closeMobile.onclick = () => toggleMobile(false);
        if (mobileOverlay) mobileOverlay.onclick = () => toggleMobile(false);

        if (userMenuBtn && dropdownMenu) {
            userMenuBtn.onclick = e => {
                e.stopPropagation();
                const open = dropdownMenu.style.display !== 'block';
                dropdownMenu.style.display = open ? 'block' : 'none';
                const c = $id('chevronIcon');
                if (c) c.style.transform = open ? 'rotate(180deg)' : '';
            };
            document.onclick = () => {
                if (dropdownMenu.style.display === 'block') {
                    dropdownMenu.style.display = 'none';
                    const c = $id('chevronIcon');
                    if (c) c.style.transform = '';
                }
            };
        }
    }

    /** Sidebar - Panel admin */
    function initSidebar() {
        const btn = $id('mobileMenuBtn');
        const sidebar = $('.sidebar');
        const overlay = $id('overlay');
        const collapse = $id('sidebarCollapseBtn');

        if (!sidebar) return;

        function toggle(open) {
            sidebar.classList.toggle('open', open);
            overlay?.classList.toggle('active', open);
            // Cambiar icono del botón
            if (btn) {
                const icon = btn.querySelector('.material-icons');
                if (icon) icon.textContent = open ? 'close' : 'menu';
                btn.classList.toggle('active', open);
            }
        }

        if (btn) btn.onclick = () => toggle(!sidebar.classList.contains('open'));
        if (overlay) overlay.onclick = () => toggle(false);

        if (collapse) {
            collapse.onclick = () => {
                sidebar.classList.toggle('collapsed');
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            };
            if (localStorage.getItem('sidebarCollapsed') === 'true') sidebar.classList.add('collapsed');
        }

        window.addEventListener('resize', () => { if (window.innerWidth > 1024) toggle(false); }, { passive: true });
    }

    /** Links activos */
    function setActiveLinks() {
        const path = window.location.pathname;
        $$('.navbar-link, .mobile-menu-link, .nav-link').forEach(l => {
            l.classList.toggle('active', l.getAttribute('href') === path);
        });
    }

    /** Dashboard */
    function initDashboard() {
        const dt = $id('currentDateTime');
        if (dt) {
            const update = () => dt.textContent = new Date().toLocaleDateString('es-CO', {
                weekday:'short', day:'numeric', month:'short', hour:'2-digit', minute:'2-digit'
            });
            update();
            setInterval(update, 60000);
        }

        const refresh = $id('refreshBtn');
        if (refresh) refresh.onclick = () => { refresh.classList.add('loading'); location.reload(); };
    }

    /** Login */
    function initLogin() {
        const toggle = $('.toggle-password');
        if (toggle) {
            toggle.onclick = function() {
                const input = $id('contrasena');
                const show = input.type === 'password';
                input.type = show ? 'text' : 'password';
                this.querySelector('.eye-icon')?.classList.toggle('hidden', show);
                this.querySelector('.eye-off-icon')?.classList.toggle('hidden', !show);
            };
        }
    }

    /** Perfil - Preview avatar y submit */
    function initPerfil() {
        const input = $id('avatarInput');
        const img = $('.profile-avatar img');
        const form = $id('avatarForm');
        if (input && img && form) {
            input.onchange = function() {
                if (this.files?.[0]) {
                    // Preview
                    const r = new FileReader();
                    r.onload = e => {
                        img.src = e.target.result;
                        // Enviar formulario después del preview
                        form.submit();
                    };
                    r.readAsDataURL(this.files[0]);
                }
            };
        }
    }

    /** Modales - Usuarios */
    window.openEditModal = btn => {
        const d = btn.dataset;
        $id('edit_id_usuario').value = d.id;
        $id('edit_nombre').value = d.nombre;
        $id('edit_correo').value = d.correo;
        $id('edit_rol').value = d.rol;
        $id('edit_estado').value = d.estado;
        SignTech.openModal('editUserModal');
    };

    window.closeEditModal = () => SignTech.closeModal('editUserModal');
    window.openCreateModal = () => SignTech.openModal('createUserModal');
    window.closeCreateModal = () => SignTech.closeModal('createUserModal');
    window.closeViewModal = () => { SignTech.closeModal('viewUserModal'); SignTech.closeModal('viewModal'); };

    /** Modal Ver - Multiplataforma */
    window.openViewModal = btn => {
        const d = btn.dataset;
        const page = document.body.dataset.page;

        if (page === 'usuarios') {
            $id('view_avatar_circle').textContent = d.nombre?.[0]?.toUpperCase() || 'U';
            $id('view_nombre_title').textContent = d.nombre;
            $id('view_correo_subtitle').textContent = d.correo;
            $id('view_nombre').textContent = d.nombre;
            $id('view_correo').textContent = d.correo;
            $id('view_documento').textContent = d.documento;
            $id('view_rol').textContent = d.rol;
            $id('view_fecha').textContent = d.fecha;
            $id('view_estado_container').innerHTML = `<span class="badge ${d.estado}">${d.estado.charAt(0).toUpperCase() + d.estado.slice(1)}</span>`;
            SignTech.openModal('viewUserModal');
        }
        else if (page === 'contribuciones') {
            $id('view_avatar').textContent = d.usuario?.[0]?.toUpperCase() || 'U';
            $id('view_palabra').textContent = d.palabra;
            $id('view_usuario').textContent = `Enviado por: ${d.usuario}`;
            $id('view_descripcion').textContent = d.descripcion;
            $id('view_fecha').textContent = SignTech.formatDate(d.fecha);

            const video = $id('view_video');
            const section = video?.closest('.view-video-section');
            if (d.video && d.video !== 'None') {
                let src = d.video;
                if (!src.startsWith('http') && !src.startsWith('/static')) src = '/static/' + src.replace(/^\//, '');
                video.src = src;
                section.style.display = 'flex';
                video.load();
            } else if (section) {
                section.style.display = 'none';
                video.src = '';
            }

            $id('view_estado_container').innerHTML = `<span class="badge ${d.estado}">${d.estado.charAt(0).toUpperCase() + d.estado.slice(1)}</span>`;

            const gestion = $id('view_gestion_item');
            if (gestion) {
                if (d.fecha_gestion && d.fecha_gestion !== 'None') {
                    $id('view_fecha_gestion').textContent = SignTech.formatDate(d.fecha_gestion);
                    gestion.style.display = 'block';
                } else gestion.style.display = 'none';
            }

            const obs = $id('view_obs_item');
            if (obs) {
                if (d.observaciones && d.observaciones !== 'None') {
                    $id('view_observaciones').textContent = d.observaciones;
                    obs.style.display = 'block';
                } else obs.style.display = 'none';
            }

            SignTech.openModal('viewModal');
        }
        else if (page === 'reportes') {
            $id('view_id').textContent = d.id;
            $id('view_descripcion').textContent = d.descripcion;
            $id('view_usuario').textContent = d.usuario || 'Anónimo';
            $id('view_fecha').textContent = d.fecha;
            $id('view_tipo').textContent = d.tipo || '-';

            const img = $id('view_img_evidencia');
            const video = $id('view_video_evidencia');
            const msg = $id('no_evidence_msg');
            img.style.display = video.style.display = msg.style.display = 'none';
            video.pause(); video.src = ''; img.src = '';

            if (d.evidencia && d.evidencia !== 'None') {
                let src = d.evidencia;
                if (!src.startsWith('http') && !src.startsWith('/static')) src = '/static/' + src.replace(/^\//, '');
                const ext = src.split('.').pop().toLowerCase();
                if (['mp4','webm','ogg','mov'].includes(ext)) {
                    video.src = src; video.style.display = 'block'; video.load();
                } else {
                    img.src = src; img.style.display = 'block';
                }
            } else msg.style.display = 'block';

            $id('view_prioridad_container').innerHTML = `<span class="priority-badge ${d.prioridad}">${d.prioridad.charAt(0).toUpperCase() + d.prioridad.slice(1)}</span>`;
            $id('view_estado_container').innerHTML = `<span class="badge ${d.estado}">${d.estado.replace('_',' ').charAt(0).toUpperCase() + d.estado.slice(1)}</span>`;

            SignTech.openModal('viewModal');
        }
    };

    /** Modal Gestionar - Contribuciones */
    window.openManageModal = btn => {
        const d = btn.dataset;
        $id('manage_id').value = d.id;
        $id('manage_palabra').textContent = d.palabra;
        SignTech.openModal('manageModal');
    };

    window.toggleObs = estado => {
        const group = $id('obs_group');
        if (group) {
            const isRechazada = estado === 'rechazada';
            group.querySelector('label').textContent = isRechazada ? 'Motivo del Rechazo (Obligatorio)' : 'Observaciones (Opcional)';
            group.querySelector('textarea').required = isRechazada;
        }
    };

    /** Eventos globales - Cerrar modales */
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') $$('.modal.active').forEach(m => SignTech.closeModal(m.id));
    });

    document.addEventListener('click', e => {
        if (e.target.classList.contains('modal') && e.target.classList.contains('active')) {
            SignTech.closeModal(e.target.id);
        }
    });

    /** Inicialización */
    function init() {
        initNavbar();
        initSidebar();
        setActiveLinks();
        initDashboard();
        initLogin();
        initPerfil();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
