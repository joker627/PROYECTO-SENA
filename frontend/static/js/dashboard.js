// ===========================
// DASHBOARD - Funcionalidad del panel de administración
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    initDashboardNotifications();
    initMobileMenu();
    initSidebarToggle();
    initDashboardRefresh(); // Inicializar actualización del dashboard
    applyChartHeights(); // Aplicar alturas del gráfico inicial
    initPdfDownloadButton(); // Inicializar botón de descarga PDF
    
    // NO ejecutar updateNotificationBadge aquí - lo hace update-badge.js globalmente
    
    // Auto-actualizar dashboard cada 5 minutos
    setInterval(refreshDashboard, 300000);
});

// ========== COLAPSAR/EXPANDIR SIDEBAR (Desktop) ==========
function initSidebarToggle() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (!sidebarToggle || !sidebar) return;

    // Solo aplicar collapsed en desktop (> 768px)
    function applyCollapsedState() {
        if (window.innerWidth > 768) {
            const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
            } else {
                sidebar.classList.remove('collapsed');
            }
        } else {
            // En móvil, siempre remover la clase collapsed
            sidebar.classList.remove('collapsed');
        }
    }

    // Aplicar estado inicial
    applyCollapsedState();

    // Aplicar estado al cambiar tamaño de ventana
    window.addEventListener('resize', applyCollapsedState);

    // Toggle sidebar al hacer clic
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        
        // Guardar estado en localStorage
        const collapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', collapsed);
    });
}

// ========== MENÚ HAMBURGUESA MÓVIL ==========
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.dashboard-overlay');

    if (!menuToggle || !sidebar) return;

    // Toggle menú al hacer clic en hamburguesa
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        menuToggle.classList.toggle('active');
        sidebar.classList.toggle('active');
        
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        // Prevenir scroll del body cuando el menú está abierto
        if (sidebar.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
    });

    // Cerrar menú al hacer clic en el overlay
    if (overlay) {
        overlay.addEventListener('click', function() {
            closeMobileMenu();
        });
    }

    // Cerrar menú al hacer clic en un enlace del sidebar
    const sidebarLinks = sidebar.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMobileMenu();
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

// ========== NOTIFICACIONES DEL DASHBOARD ==========
function initDashboardNotifications() {
    const notificationsBtn = document.querySelector('.notifications');
    const headerRight = document.querySelector('.header-right');

    if (!notificationsBtn || !headerRight) return;

    // Toggle notificaciones al hacer clic
    notificationsBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        headerRight.classList.toggle('notifications-active');
    });

    // Cerrar dropdown al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!headerRight.contains(e.target)) {
            headerRight.classList.remove('notifications-active');
        }
    });

    // Cerrar con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && headerRight.classList.contains('notifications-active')) {
            headerRight.classList.remove('notifications-active');
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
            
            // Actualizar badge en la campana del header del dashboard
            const dashboardBadge = document.querySelector('.notifications .notification-badge');
            if (dashboardBadge) {
                dashboardBadge.textContent = count;
                dashboardBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // Actualizar badge en el slider/sidebar (por ID)
            const sliderBadge = document.getElementById('sliderNotificationBadge');
            if (sliderBadge) {
                sliderBadge.textContent = count;
                sliderBadge.style.display = count > 0 ? 'inline-flex' : 'none';
            }
            
            // Actualizar todos los badges .menu-badge en enlaces de notificaciones
            const menuBadges = document.querySelectorAll('.menu-badge');
            menuBadges.forEach(badge => {
                const parentLink = badge.closest('a');
                if (parentLink && parentLink.href.includes('notifications')) {
                    badge.textContent = count;
                    badge.style.display = count > 0 ? 'flex' : 'none';
                }
            });
            
            console.log(`[DASHBOARD] Badge actualizado: ${count} notificaciones`);
        }
    } catch (error) {
        console.error('Error al actualizar badge de notificaciones:', error);
    }
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
        const response = await fetch('/admin/api/dashboard-data');
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            
            // Actualizar métricas
            updateMetricsCards(data.metrics);
            
            // Actualizar actividad reciente
            updateActivityList(data.activity);
            
            // Actualizar gráfico
            updateChart(data.chart);
            
            // Actualizar proyectos
            updateProjects(data.projects);
            
            // Actualizar timestamp
            updateLastUpdateTime();
            
            // Mostrar toast de éxito
            toastSuccess('Dashboard actualizado correctamente', 'Actualización exitosa');
        } else {
            toastError('Error al actualizar el dashboard', 'Error de actualización');
        }
    } catch (error) {
        console.error('Error al actualizar dashboard:', error);
        toastError('Error de conexión al actualizar', 'Error de conexión');
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
    
    const precisionStatus = metrics.precision.average >= 90 ? 'excellent' : metrics.precision.average >= 75 ? 'good' : 'warning';
    const precisionTrend = precisionStatus === 'excellent' ? 'positive' : precisionStatus === 'good' ? 'neutral' : 'negative';
    const precisionIcon = precisionStatus === 'excellent' ? 'check' : precisionStatus === 'good' ? 'minus' : 'exclamation';
    const precisionText = precisionStatus === 'excellent' ? 'Excelente' : precisionStatus === 'good' ? 'Bueno' : 'Necesita mejora';
    
    container.innerHTML = `
        <div class="card user-card">
            <div class="card-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="card-content">
                <h3>Usuarios</h3>
                <p class="card-description">Total registrados</p>
                <span class="card-value">${metrics.users.total}</span>
                <div class="card-trend ${metrics.users.trend}">
                    <i class="fas fa-arrow-${metrics.users.trend === 'positive' ? 'up' : 'down'}"></i>
                    <span>${Math.abs(metrics.users.growth)}% este mes</span>
                </div>
            </div>
        </div>
        <div class="card translations-card">
            <div class="card-icon">
                <i class="fas fa-language"></i>
            </div>
            <div class="card-content">
                <h3>Traducciones</h3>
                <p class="card-description">Total realizadas</p>
                <span class="card-value">${metrics.translations.total}</span>
                <div class="card-trend ${metrics.translations.trend}">
                    <i class="fas fa-arrow-${metrics.translations.trend === 'positive' ? 'up' : 'down'}"></i>
                    <span>${Math.abs(metrics.translations.growth)}% este mes</span>
                </div>
            </div>
        </div>
        <div class="card anonymous-card">
            <div class="card-icon">
                <i class="fas fa-user-secret"></i>
            </div>
            <div class="card-content">
                <h3>Usuarios Anónimos</h3>
                <p class="card-description">Registrados</p>
                <span class="card-value">${metrics.anonymous.total}</span>
                <div class="card-trend neutral">
                    <i class="fas fa-chart-line"></i>
                    <span>Total acumulado</span>
                </div>
            </div>
        </div>
        <div class="card precision-card">
            <div class="card-icon">
                <i class="fas fa-bullseye"></i>
            </div>
            <div class="card-content">
                <h3>Precisión Modelo</h3>
                <p class="card-description">Promedio</p>
                <span class="card-value">${metrics.precision.average}%</span>
                <div class="card-trend ${precisionTrend}">
                    <i class="fas fa-${precisionIcon}"></i>
                    <span>${precisionText}</span>
                </div>
            </div>
        </div>
        <div class="card project-card">
            <div class="card-icon">
                <i class="fas fa-project-diagram"></i>
            </div>
            <div class="card-content">
                <h3>Contribuciones</h3>
                <p class="card-description">Validadas</p>
                <span class="card-value">${metrics.projects.total}</span>
                <div class="card-trend ${metrics.projects.trend}">
                    <i class="fas fa-arrow-${metrics.projects.trend === 'positive' ? 'up' : 'down'}"></i>
                    <span>${Math.abs(metrics.projects.growth)}% este mes</span>
                </div>
            </div>
        </div>
        <div class="card colaboradores-card">
            <div class="card-icon">
                <i class="fas fa-user-tie"></i>
            </div>
            <div class="card-content">
                <h3>Colaboradores</h3>
                <p class="card-description">Activos</p>
                <span class="card-value">${metrics.colaboradores.total}</span>
                <div class="card-trend neutral">
                    <i class="fas fa-users"></i>
                    <span>Total activos</span>
                </div>
            </div>
        </div>
        <div class="card report-card">
            <div class="card-icon">
                <i class="fas fa-chart-bar"></i>
            </div>
            <div class="card-content">
                <h3>Reportes</h3>
                <p class="card-description">Pendientes</p>
                <span class="card-value">${metrics.reports.total}</span>
                <div class="card-trend ${metrics.reports.trend}">
                    <i class="fas fa-arrow-${metrics.reports.trend === 'positive' ? 'down' : 'up'}"></i>
                    <span>${Math.abs(metrics.reports.change)}% este mes</span>
                </div>
            </div>
        </div>
        <div class="card performance-card">
            <div class="card-icon">
                <i class="fas fa-bell"></i>
            </div>
            <div class="card-content">
                <h3>Alertas Sistema</h3>
                <p class="card-description">No resueltas</p>
                <span class="card-value">${metrics.alerts.total}</span>
                <div class="card-trend ${metrics.alerts.total === 0 ? 'neutral' : 'negative'}">
                    <i class="fas fa-${metrics.alerts.total === 0 ? 'check' : 'exclamation'}"></i>
                    <span>${metrics.alerts.total === 0 ? 'Todo bien' : 'Requiere atención'}</span>
                </div>
            </div>
        </div>
        <div class="card solicitudes-card">
            <div class="card-icon">
                <i class="fas fa-user-plus"></i>
            </div>
            <div class="card-content">
                <h3>Solicitudes</h3>
                <p class="card-description">Pendientes</p>
                <span class="card-value">${metrics.solicitudes.total}</span>
                <div class="card-trend ${metrics.solicitudes.total === 0 ? 'neutral' : 'pending'}">
                    <i class="fas fa-${metrics.solicitudes.total === 0 ? 'check' : 'clock'}"></i>
                    <span>${metrics.solicitudes.total === 0 ? 'Sin pendientes' : 'Revisar'}</span>
                </div>
            </div>
        </div>
    `;
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
                <p class="project-description">${project.descripcion.substring(0, 80)}${project.descripcion.length > 80 ? '...' : ''}</p>
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
