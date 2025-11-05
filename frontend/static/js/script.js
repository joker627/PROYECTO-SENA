// Inicialización del dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeSidebar();
    loadDashboardData();
});

// Configuración de gráficos
function initializeCharts() {
    const ctx = document.getElementById('traduccionesChart').getContext('2d');
    
    // Datos de ejemplo para el gráfico
    const data = {
        labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        datasets: [
            {
                label: 'Señas → Texto',
                data: [65, 78, 90, 81, 86, 55, 40],
                borderColor: '#2c5aa0',
                backgroundColor: 'rgba(44, 90, 160, 0.1)',
                tension: 0.4,
                fill: true
            },
            {
                label: 'Texto → Señas',
                data: [45, 62, 75, 70, 68, 45, 30],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4,
                fill: true
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

// Funcionalidad del sidebar móvil
function initializeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const navItems = document.querySelectorAll('.nav-item');
    
    // Activar elemento del menú al hacer clic
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Toggle sidebar en móvil
    if (window.innerWidth <= 768) {
        document.addEventListener('click', function(e) {
            if (e.target.closest('.menu-toggle')) {
                sidebar.classList.toggle('active');
            }
        });
    }
}

// Cargar datos del dashboard
function loadDashboardData() {
    // Simular carga de datos
    console.log('Cargando datos del dashboard...');
    
    // Aquí irían las llamadas a la API para cargar datos reales
    // fetch('/api/dashboard/stats')
    //   .then(response => response.json())
    //   .then(data => updateDashboard(data));
}

// Actualizar estadísticas del dashboard
function updateDashboard(data) {
    // Actualizar tarjetas de estadísticas
    const statCards = document.querySelectorAll('.stat-card h3');
    
    // Ejemplo de actualización
    if (data.totalUsers) {
        statCards[0].textContent = data.totalUsers.toLocaleString();
    }
    
    if (data.totalTranslations) {
        statCards[1].textContent = data.totalTranslations.toLocaleString();
    }
    
    // ... más actualizaciones
}

// Funciones de utilidad
function formatNumber(num) {
    return num.toLocaleString();
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('es-ES');
}

// Manejo de notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Exportar funciones para uso global
window.AdminDashboard = {
    initializeCharts,
    loadDashboardData,
    showNotification
};