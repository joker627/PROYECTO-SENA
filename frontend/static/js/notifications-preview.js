// Script para cargar vista previa de notificaciones en navbar y dashboard

function loadNotificationsPreview() {
    fetch('/notifications/preview')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateNotificationsDropdown(data.notifications);
            } else {
                console.error('Error al cargar notificaciones:', data.error);
            }
        })
        .catch(error => {
            console.error('Error en la petición de notificaciones:', error);
        });
}

function updateNotificationsDropdown(notifications) {
    // Buscar todos los contenedores de notificaciones en la página
    // Incluye tanto .notifications-dropdown como .dashboard-notifications-dropdown
    const dropdowns = document.querySelectorAll('.notifications-dropdown, .dashboard-notifications-dropdown');
    
    dropdowns.forEach(dropdown => {
        // Buscar el contenedor de la lista dentro del dropdown
        const listContainer = dropdown.querySelector('.notifications-list');
        
        if (!listContainer) return;
        
        // Limpiar contenido existente
        listContainer.innerHTML = '';
        
        if (notifications.length === 0) {
            // Si no hay notificaciones
            listContainer.innerHTML = `
                <div class="notification-item" style="text-align: center; padding: 20px; color: #888;">
                    <i class="fas fa-inbox" style="font-size: 24px; margin-bottom: 10px;"></i>
                    <p style="margin: 0;">No hay alertas pendientes</p>
                </div>
            `;
        } else {
            // Agregar cada notificación
            notifications.forEach(notif => {
                const notifElement = document.createElement('div');
                notifElement.className = 'notification-item' + (notif.is_unread ? ' unread' : '');
                
                // Determinar color del badge según severidad
                let badgeClass = 'badge-info';
                let badgeStyle = 'background: #17a2b8; color: white;';
                if (notif.severidad === 'crítico') {
                    badgeClass = 'badge-error';
                    badgeStyle = 'background: #dc3545; color: white;';
                } else if (notif.severidad === 'alto') {
                    badgeClass = 'badge-warning';
                    badgeStyle = 'background: #ffc107; color: black;';
                }
                
                notifElement.innerHTML = `
                    <div class="notification-icon">
                        <i class="fas ${notif.icon}"></i>
                    </div>
                    <div class="notification-content">
                        <p class="notification-title">
                            ${notif.title}
                            <span class="${badgeClass}" style="${badgeStyle} padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-left: 8px;">${notif.severidad.toUpperCase()}</span>
                        </p>
                        <p class="notification-text">${notif.text}</p>
                        <span class="notification-time">${notif.time}</span>
                    </div>
                `;
                
                // Hacer que la notificación sea clickeable
                notifElement.style.cursor = 'pointer';
                notifElement.addEventListener('click', () => {
                    window.location.href = '/notifications';
                });
                
                listContainer.appendChild(notifElement);
            });
        }
    });
}

// Cargar notificaciones al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    loadNotificationsPreview();
    
});
