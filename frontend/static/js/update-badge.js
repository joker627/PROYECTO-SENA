// ===========================
// ACTUALIZAR BADGES DE NOTIFICACIONES Y REPORTES - Script global
// ===========================

// Ejecutar inmediatamente al cargar
(function() {
    updateAllNotificationBadges();
    updateReportesBadge();
    updateNotificationsPreview(); // Actualizar preview de notificaciones

    // Actualizar cada 5 segundos (optimizado para mejor rendimiento)
    // ESTE ES EL ÚNICO TIMER GLOBAL PARA NOTIFICACIONES
    setInterval(() => {
        updateAllNotificationBadges();
        updateReportesBadge();
        updateNotificationsPreview(); // Actualizar preview de notificaciones
    }, 5000);
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
            // Ensure CSS "hidden" class (which may use !important) is in sync
            if (count > 0) sliderReportesBadge.classList.remove('hidden'); else sliderReportesBadge.classList.add('hidden');
        }
        
        // Todos los badges en enlaces de reportes
        const reportesLinks = document.querySelectorAll('a[href*="reportes"]');
        reportesLinks.forEach(link => {
            const badge = link.querySelector('.menu-badge');
            if (badge) {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
                if (count > 0) badge.classList.remove('hidden'); else badge.classList.add('hidden');
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
                // Sync hidden class so stylesheet with !important doesn't keep it hidden
                if (count > 0) sliderBadge.classList.remove('hidden'); else sliderBadge.classList.add('hidden');
            }
            
            // 2. Todos los badges en enlaces de notificaciones
            const notificationLinks = document.querySelectorAll('a[href*="notifications"]');
            notificationLinks.forEach(link => {
                const badge = link.querySelector('.menu-badge');
                if (badge) {
                    badge.textContent = count;
                    badge.style.display = count > 0 ? 'flex' : 'none';
                    if (count > 0) badge.classList.remove('hidden'); else badge.classList.add('hidden');
                }
            });

        
            // cuyo enlace padre (closest <a>) contenga 'notifications' en el href.
            const allMenuBadges = document.querySelectorAll('.menu .menu-item .menu-badge');
            allMenuBadges.forEach(badge => {
                try {
                    const parentLink = badge.closest('a');
                    const href = parentLink ? parentLink.getAttribute('href') || '' : '';
                    if (href.includes('notifications') || badge.id === 'sliderNotificationBadge') {
                        badge.textContent = count;
                        badge.style.display = count > 0 ? 'flex' : 'none';
                        if (count > 0) badge.classList.remove('hidden'); else badge.classList.add('hidden');
                    }
                } catch (e) {
                    // ignore
                }
            });
            
            // 3. Badge de la campana en el navbar y dashboard (clase unificada)
            const notificationBadges = document.querySelectorAll('.notification-badge');
            notificationBadges.forEach(badge => {
                badge.textContent = count;
                if (count > 0) {
                    badge.style.display = 'inline-block';
                    badge.classList.remove('hidden');
                } else {
                    badge.style.display = 'none';
                    badge.classList.add('hidden');
                }
            });
            
            // 4. Badge móvil
            const mobileBadges = document.querySelectorAll('.mobile-notification-badge');
            mobileBadges.forEach(badge => {
                badge.textContent = count;
                if (count > 0) {
                    badge.style.display = 'inline-block';
                    badge.classList.remove('hidden');
                } else {
                    badge.style.display = 'none';
                    badge.classList.add('hidden');
                }
            });
            
            // 5. Badge en navbar con clase específica (si existe)
            const navbarBadge = document.querySelector('.notifications-btn .menu-badge');
            if (navbarBadge) {
                navbarBadge.textContent = count;
                navbarBadge.style.display = count > 0 ? 'flex' : 'none';
                if (count > 0) navbarBadge.classList.remove('hidden'); else navbarBadge.classList.add('hidden');
            }
            
            // 6. Badge en móvil con clase específica (si existe)
            const mobileBadge = document.querySelector('.mobile-notifications-btn .menu-badge');
            if (mobileBadge) {
                mobileBadge.textContent = count;
                mobileBadge.style.display = count > 0 ? 'flex' : 'none';
                if (count > 0) mobileBadge.classList.remove('hidden'); else mobileBadge.classList.add('hidden');
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
