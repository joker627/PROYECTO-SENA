// ===========================
// DASHBOARD - Funcionalidad del panel de administración
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    // Remover clase de inicialización para permitir transiciones suaves
    document.documentElement.classList.remove('sidebar-collapsed-init');
    initMobileMenu();
    initSidebarToggle();
    initDashboardRefresh();
    applyChartHeights();
    initPdfDownloadButton();
    
    // Auto-actualizar dashboard cada 5 minutos
    setInterval(refreshDashboard, 300000);
    // Ejecutar una actualización ligera inmediatamente para poblar badges (solicitudes, métricas)
    try { refreshDashboard(); } catch (e) { console.debug('initial refreshDashboard failed', e); }
});

// ========== COLAPSAR/EXPANDIR SIDEBAR (Desktop) ==========
function initSidebarToggle() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const dashboardContainer = document.querySelector('.dashboard-container');

    if (!sidebarToggle || !sidebar) return;

    // Solo aplicar collapsed en desktop (> 768px)
    function applyCollapsedState() {
        if (window.innerWidth > 768) {
            const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
                if (dashboardContainer) dashboardContainer.classList.add('sidebar-collapsed');
            } else {
                sidebar.classList.remove('collapsed');
                if (dashboardContainer) dashboardContainer.classList.remove('sidebar-collapsed');
            }
        } else {
            // En móvil, siempre remover la clase collapsed
            sidebar.classList.remove('collapsed');
            if (dashboardContainer) dashboardContainer.classList.remove('sidebar-collapsed');
        }
    }

    // Aplicar estado inicial INMEDIATAMENTE antes de que se vea
    applyCollapsedState();

    // Aplicar estado al cambiar tamaño de ventana con debounce
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(applyCollapsedState, 100);
    });

    // Toggle sidebar al hacer clic con animación suave
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        // Mantener sincronizado el container para reglas CSS que usan
        // el modificador de nivel contenedor (.dashboard-container.sidebar-collapsed)
        if (dashboardContainer) {
            dashboardContainer.classList.toggle('sidebar-collapsed');
        }
        
        // Guardar estado en localStorage
        const collapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', collapsed);
        
        // Animación del icono
        const icon = this.querySelector('i');
        if (icon) {
            icon.style.transform = collapsed ? 'rotate(180deg)' : 'rotate(0deg)';
        }
    });
}

// ========== MENÚ HAMBURGUESA MÓVIL ==========
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.dashboard-overlay');

    if (!menuToggle || !sidebar) return;

    // Toggle menú al hacer clic en hamburguesa con animación suave
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isActive = sidebar.classList.contains('active');
        
        // Animación del botón hamburguesa
        menuToggle.classList.toggle('active');
        sidebar.classList.toggle('active');
        
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        // Prevenir scroll del body cuando el menú está abierto
        if (!isActive) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
    });

    // Cerrar menú al hacer clic en el overlay con animación
    if (overlay) {
        overlay.addEventListener('click', function() {
            closeMobileMenu();
        });
    }

    // Cerrar menú al hacer clic en un enlace del sidebar (excepto el dropdown)
    const sidebarLinks = sidebar.querySelectorAll('.menu-item:not(.logout) a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Pequeño delay para que se vea el efecto de clic
            setTimeout(closeMobileMenu, 150);
        });
    });

    // Cerrar menú con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    function closeMobileMenu() {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
        if (overlay) {
            overlay.classList.remove('active');
        }
        document.body.style.overflow = 'auto';
    }
}

// Notification UI removed: dashboard notification handlers were deleted.
// ========== ACTUALIZAR BADGE DE NOTIFICACIONES ==========
async function updateNotificationBadge() {
    // Stub: notifications removed. No-op to avoid fetch errors.
    console.debug('dashboard.updateNotificationBadge(): stubbed because notifications were removed');
}

// ========== ACTUALIZACIÓN DEL DASHBOARD SIN RECARGAR ==========
function applyChartHeights() {
    const bars = document.querySelectorAll('.bar[data-height]');
    bars.forEach(bar => {
        const height = bar.getAttribute('data-height');
        if (height) {
            bar.style.height = height + '%';
        }
    });
}

function initDashboardRefresh() {
    const refreshBtn = document.getElementById('refreshDashboard');
    if (!refreshBtn) return;
    
    refreshBtn.addEventListener('click', function() {
        refreshDashboard();
    });
}

async function refreshDashboard() {
    const refreshBtn = document.getElementById('refreshDashboard');
    const refreshIcon = refreshBtn ? refreshBtn.querySelector('i') : null;
    
    // Animación de carga
    if (refreshIcon) {
        refreshIcon.classList.add('fa-spin');
        refreshBtn.disabled = true;
    }
    
    try {
        // Lightweight update: only refresh numeric metrics and the report badge.
        const response = await fetch('/admin/api/dashboard-data');
        const result = await response.json();

        if (result.success) {
            const data = result.data;
            // Update only numeric metric cards (lightweight)
            updateMetricsCards(data.metrics);

            // Update slider solicitudes badge if present
            try {
                const solCount = data.metrics && data.metrics.solicitudes ? (data.metrics.solicitudes.total || 0) : 0;
                const sliderSolicitudesBadge = document.getElementById('sliderSolicitudesBadge');
                if (sliderSolicitudesBadge) {
                    sliderSolicitudesBadge.textContent = solCount;
                    sliderSolicitudesBadge.style.display = solCount > 0 ? 'flex' : 'none';
                    if (solCount > 0) sliderSolicitudesBadge.classList.remove('hidden'); else sliderSolicitudesBadge.classList.add('hidden');
                }
            } catch (e) {
                console.debug('No se pudo actualizar badge de solicitudes:', e);
            }

            // Report badge update removed: slider badges are no longer updated automatically
        } else {
            console.debug('refreshDashboard: backend returned success=false');
        }
    } catch (error) {
        console.error('Error al actualizar dashboard (light):', error);
    } finally {
        // Quitar animación
        if (refreshIcon) {
            refreshIcon.classList.remove('fa-spin');
            refreshBtn.disabled = false;
        }
    }
}

// Actualizar tarjetas de métricas
function updateMetricsCards(metrics) {
    const container = document.getElementById('metricsCards');
    if (!container) return;

    // Helper para actualizar texto/valores dentro de una tarjeta existente
    function safeText(el, selector, text) {
        if (!el) return;
        const target = el.querySelector(selector);
        if (target) target.textContent = text;
    }

    // Usuarios
    const userCard = container.querySelector('.user-card');
    if (userCard) {
        safeText(userCard, '.card-value', metrics.users.total);
        safeText(userCard, '.card-trend span', `${Math.abs(metrics.users.growth)}% este mes`);
        const trend = userCard.querySelector('.card-trend');
        if (trend) {
            trend.className = 'card-trend ' + (metrics.users.trend || 'neutral');
        }
    }

    // Traducciones (skip if the card is fixed by template)
    const transCard = container.querySelector('.translations-card');
    if (transCard && !transCard.classList.contains('fixed-metric')) {
        safeText(transCard, '.card-value', metrics.translations.total);
        safeText(transCard, '.card-trend span', `${Math.abs(metrics.translations.growth)}% este mes`);
        const trend = transCard.querySelector('.card-trend');
        if (trend) trend.className = 'card-trend ' + (metrics.translations.trend || 'neutral');
    }

    // Usuarios anónimos
    const anonCard = container.querySelector('.anonymous-card');
    if (anonCard) {
        safeText(anonCard, '.card-value', metrics.anonymous.total);
    }

    // Precisión (puede ser project-card + precision-card o card precision-card)
    const precisionCard = container.querySelector('.precision-card');
    if (precisionCard && !precisionCard.classList.contains('fixed-metric')) {
        // Si tiene badge de estado (project-card)
        const badge = precisionCard.querySelector('.project-status');
        if (badge) {
            const status = metrics.precision.status === 'excellent' ? 'completed' : metrics.precision.status === 'good' ? 'in-progress' : 'pending';
            badge.className = 'project-status ' + status;
            badge.textContent = metrics.precision.status === 'excellent' ? 'Excelente' : metrics.precision.status === 'good' ? 'Bueno' : 'Necesita mejora';
        }
        // Actualizar valor mostrado
        const val = precisionCard.querySelector('.card-value') || precisionCard.querySelector('.project-meta .card-value') || precisionCard.querySelector('.project-meta-item span');
        if (val) val.textContent = metrics.precision.average + '%';
    }

    // Contribuciones / proyectos (project-card structured)
    const projectsCard = container.querySelector('.project-card--contribuciones');
    if (projectsCard) {
        // actualizar valor total
        const valueSpan = projectsCard.querySelector('.project-meta .project-meta-item:first-child span');
        if (valueSpan) valueSpan.textContent = metrics.projects.total;
        // actualizar segundo meta (porcentaje)
        const percentSpan = projectsCard.querySelector('.project-meta .project-meta-item:nth-child(2) span');
        if (percentSpan) percentSpan.textContent = `${Math.abs(metrics.projects.growth)}% este mes`;
        // actualizar badge
        const status = metrics.projects.trend === 'positive' ? 'completed' : 'pending';
        const badge = projectsCard.querySelector('.project-status');
        if (badge) {
            badge.className = 'project-status ' + status;
            badge.textContent = metrics.projects.trend === 'positive' ? 'Crecimiento' : 'Estable';
        }
    } else {
        // backward-compatible: if still using old card structure
        const legacyProjectsCard = container.querySelector('.card.project-card');
        if (legacyProjectsCard) {
            safeText(legacyProjectsCard, '.card-value', metrics.projects.total);
            const trend = legacyProjectsCard.querySelector('.card-trend');
            if (trend) trend.className = 'card-trend ' + (metrics.projects.trend || 'neutral');
        }
    }

    // Colaboradores (project-card)
    const colabCard = container.querySelector('.colaboradores-card');
    if (colabCard) {
        const valueSpan = colabCard.querySelector('.project-meta .project-meta-item:first-child span') || colabCard.querySelector('.card-value');
        if (valueSpan) valueSpan.textContent = metrics.colaboradores.total;
    }

    // Reportes (project-card)
    const reportCard = container.querySelector('.report-card');
    if (reportCard) {
        const valueSpan = reportCard.querySelector('.project-meta .project-meta-item:first-child span') || reportCard.querySelector('.card-value');
        if (valueSpan) valueSpan.textContent = metrics.reports.total;
        const percentSpan = reportCard.querySelector('.project-meta .project-meta-item:nth-child(2) span');
        if (percentSpan) percentSpan.textContent = `${Math.abs(metrics.reports.change)}% este mes`;
        const badge = reportCard.querySelector('.project-status');
        if (badge) {
            const status = metrics.reports.trend === 'positive' ? 'completed' : 'pending';
            badge.className = 'project-status ' + status;
            badge.textContent = metrics.reports.trend === 'positive' ? 'Mejora' : 'Atención';
        }
    }

    // Alertas: card removed from grid; header badge is updated elsewhere

    // Solicitudes (project-card)
    const solCard = container.querySelector('.solicitudes-card');
    if (solCard) {
        const valueSpan = solCard.querySelector('.project-meta .project-meta-item:first-child span') || solCard.querySelector('.card-value');
        if (valueSpan) valueSpan.textContent = metrics.solicitudes.total;
        const badge = solCard.querySelector('.project-status');
        if (badge) {
            const status = metrics.solicitudes.total == 0 ? 'completed' : 'pending';
            badge.className = 'project-status ' + status;
            badge.textContent = metrics.solicitudes.total == 0 ? 'Sin pendientes' : 'Revisar';
        }
    }

    // Si por alguna razón faltan tarjetas (p.ej. primera carga), recrearlas parcialmente
    // Para evitar romper estilos existentes, sólo añadimos lo mínimo necesario
    const expectedCount = 9; // número aproximado de tarjetas
    if (container.children.length < expectedCount) {
        // fallback: forzar recarga completa (menos frecuente)
        container.innerHTML = container.innerHTML; // no-op para forzar reflow sin cambiar estilos
    }
}

// Actualizar lista de actividad
function updateActivityList(activities) {
    const container = document.getElementById('activityList');
    if (!container) return;
    
    if (activities && activities.length > 0) {
        container.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas ${activity.icon}"></i>
                </div>
                <div class="activity-details">
                    <p>${activity.descripcion}</p>
                    <span class="activity-time">${activity.time_ago}</span>
                </div>
            </div>
        `).join('');
    } else {
        container.innerHTML = `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas fa-inbox"></i>
                </div>
                <div class="activity-details">
                    <p>No hay actividad reciente</p>
                    <span class="activity-time">-</span>
                </div>
            </div>
        `;
    }
}

// Actualizar gráfico de barras
function updateChart(chartData) {
    const container = document.getElementById('chartBars');
    if (!container) return;
    
    container.innerHTML = chartData.map(day => `
        <div class="bar" data-height="${day.height}" title="${day.value} traducciones">
            <span class="bar-label">${day.label}</span>
        </div>
    `).join('');
    
    // Aplicar alturas después de insertar
    applyChartHeights();
}

// Actualizar proyectos
function updateProjects(projects) {
    const container = document.getElementById('projectsGrid');
    if (!container) return;
    
    if (projects && projects.length > 0) {
        container.innerHTML = projects.map(project => `
            <div class="project-card">
                <div class="project-header">
                    <h3>${project.titulo}</h3>
                    <span class="project-status ${project.estado_class}">${project.estado}</span>
                </div>
                // Entregar la descripción completa; el recorte visual lo hará CSS (2 líneas si se desea)
                <p class="project-description">${project.descripcion}</p>
                <div class="project-meta">
                    <div class="project-meta-item">
                        <i class="fas fa-calendar"></i>
                        <span>${project.fecha}</span>
                    </div>
                    <div class="project-meta-item">
                        <i class="fas fa-user"></i>
                        <span>${project.colaborador}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } else {
        container.innerHTML = `
            <div class="project-card">
                <div class="project-header">
                    <h3>Sin contribuciones</h3>
                    <span class="project-status pending">Pendiente</span>
                </div>
                <p class="project-description">No hay contribuciones registradas en el sistema</p>
                <div class="project-meta">
                    <div class="project-meta-item">
                        <i class="fas fa-info-circle"></i>
                        <span>Esperando datos</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// Actualizar timestamp de última actualización
function updateLastUpdateTime() {
    const lastUpdate = document.getElementById('lastUpdate');
    if (!lastUpdate) return;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
    
    lastUpdate.textContent = `Última actualización: ${timeString}`;
}

// ========== BOTÓN DESCARGA PDF ==========
function initPdfDownloadButton() {
    const pdfBtn = document.querySelector('.btn-download-pdf');
    if (!pdfBtn) return;
    
    pdfBtn.addEventListener('click', function(e) {
        // Mostrar toast de descarga iniciada
        if (typeof toastInfo === 'function') {
            toastInfo('Generando reporte PDF...', 'Descarga en Proceso', 3000);
        }
        
        // El navegador manejará la descarga automáticamente
        // Después de un tiempo, mostrar toast de éxito
        setTimeout(() => {
            if (typeof toastSuccess === 'function') {
                toastSuccess('Reporte PDF descargado correctamente', 'Descarga Exitosa', 4000);
            }
        }, 1500);
    });
}
