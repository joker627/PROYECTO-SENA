// ===========================
// ACTUALIZAR BADGES DE NOTIFICACIONES Y REPORTES - Script global
// ===========================

// Ejecutar inmediatamente al cargar
(function() {
    updateAllNotificationBadges();
    updateReportesBadge();
    updateNotificationsPreview(); // Actualizar preview de notificaciones
    
    // Actualizar cada 60 segundos (optimizado para mejor rendimiento)
    // ESTE ES EL ÚNICO TIMER GLOBAL PARA NOTIFICACIONES
    setInterval(() => {
        updateAllNotificationBadges();
        updateReportesBadge();
        updateNotificationsPreview(); // Actualizar preview de notificaciones
    }, 60000);
})();

// Función para actualizar badge de reportes
async function updateReportesBadge() {
    try {
        const response = await fetch('/reportes/api/count');
        const data = await response.json();
        
        const count = data.count || 0;
        console.log('Actualizando badge de reportes con conteo:', count);
        
        // Badge del slider de reportes
        const sliderReportesBadge = document.getElementById('sliderReportesBadge');
        if (sliderReportesBadge) {
            sliderReportesBadge.textContent = count;
            sliderReportesBadge.style.display = count > 0 ? 'flex' : 'none';
        }
        
        // Todos los badges en enlaces de reportes
        const reportesLinks = document.querySelectorAll('a[href*="reportes"]');
        reportesLinks.forEach(link => {
            const badge = link.querySelector('.menu-badge');
            if (badge) {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
            }
        });
        
        console.log('Badge de reportes actualizado exitosamente');
    } catch (error) {
        console.error('Error al actualizar badge de reportes:', error);
    }
}

// Función principal para actualizar todos los badges de notificaciones
async function updateAllNotificationBadges() {
    try {
        const response = await fetch('/notifications/count');
        const data = await response.json();
        
        if (data.success) {
            const count = data.count;
            console.log('Actualizando badges de notificaciones con conteo:', count);
            
            // 1. Badge del slider (ID específico)
            const sliderBadge = document.getElementById('sliderNotificationBadge');
            if (sliderBadge) {
                sliderBadge.textContent = count;
                sliderBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // 2. Todos los badges en enlaces de notificaciones
            const notificationLinks = document.querySelectorAll('a[href*="notifications"]');
            notificationLinks.forEach(link => {
                const badge = link.querySelector('.menu-badge');
                if (badge) {
                    badge.textContent = count;
                    badge.style.display = count > 0 ? 'flex' : 'none';
                }
            });
            
            // 3. Badge de la campana en el header del dashboard
            const notificationBadge = document.querySelector('.notification-badge');
            if (notificationBadge) {
                notificationBadge.textContent = count;
                notificationBadge.style.display = count > 0 ? 'inline-block' : 'none';
            }
            
            // 4. Badge en navbar (si existe)
            const navbarBadge = document.querySelector('.notifications-btn .menu-badge');
            if (navbarBadge) {
                navbarBadge.textContent = count;
                navbarBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            // 5. Badge en móvil (si existe)
            const mobileBadge = document.querySelector('.mobile-notifications-btn .menu-badge');
            if (mobileBadge) {
                mobileBadge.textContent = count;
                mobileBadge.style.display = count > 0 ? 'flex' : 'none';
            }
            
            console.log('Badges de notificaciones actualizados exitosamente');
        }
    } catch (error) {
        console.error('Error al actualizar badges de notificaciones:', error);
    }
}

// Función para actualizar el preview de notificaciones (si existe loadNotificationsPreview)
function updateNotificationsPreview() {
    if (typeof loadNotificationsPreview === 'function') {
        loadNotificationsPreview();
    }
}

// Hacer las funciones globales
window.updateAllNotificationBadges = updateAllNotificationBadges;
window.updateReportesBadge = updateReportesBadge;
window.updateNotificationsPreview = updateNotificationsPreview;
