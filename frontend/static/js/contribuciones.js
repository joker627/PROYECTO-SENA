/**
 * Maneja las interacciones de la página de contribuciones.
 */

function formatFecha(fechaStr) {
    if (!fechaStr || fechaStr === 'None') return '-';
    try {
        const date = new Date(fechaStr);
        if (isNaN(date.getTime())) return fechaStr;
        return date.toLocaleString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return fechaStr;
    }
}

function openViewModal(btn) {
    const modal = document.getElementById('viewModal');

    // Extraer datos
    const usuario = btn.dataset.usuario;
    const palabra = btn.dataset.palabra;
    const descripcion = btn.dataset.descripcion;
    const fecha = btn.dataset.fecha;
    const estado = btn.dataset.estado;
    const video = btn.dataset.video;
    const fecha_gestion = btn.dataset.fecha_gestion;
    const observaciones = btn.dataset.observaciones;

    // Poblar modal
    document.getElementById('view_avatar').textContent = usuario ? usuario[0].toUpperCase() : 'U';
    document.getElementById('view_palabra').textContent = palabra;
    document.getElementById('view_usuario').textContent = `Enviado por: ${usuario}`;
    document.getElementById('view_descripcion').textContent = descripcion;
    document.getElementById('view_fecha').textContent = formatFecha(fecha);

    // Video Path Handling (Directo desde DB)
    const videoElement = document.getElementById('view_video');
    const videoSection = videoElement.closest('.view-video-section');

    if (video && video !== 'None' && video !== '') {
        let videoSrc = video;

        // Si el path no empieza por http y es relativo, asegurar que apunte a static
        if (!videoSrc.startsWith('http')) {
            if (!videoSrc.startsWith('/static')) {
                // Si ya empieza por /, solo anteponer /static
                if (videoSrc.startsWith('/')) {
                    videoSrc = '/static' + videoSrc;
                } else {
                    videoSrc = '/static/' + videoSrc;
                }
            }
        }

        videoElement.src = videoSrc;
        videoSection.style.display = 'flex';
        videoElement.load(); // Forzar recarga del recurso
    } else {
        // Si no hay video en la DB, ocultar la sección de video por completo
        videoSection.style.display = 'none';
        videoElement.src = "";
    }

    // Badge de estado
    const container = document.getElementById('view_estado_container');
    const label = estado.charAt(0).toUpperCase() + estado.slice(1);
    container.innerHTML = `<span class="badge ${estado}">${label}</span>`;

    // Gestión
    const gestionItem = document.getElementById('view_gestion_item');
    if (fecha_gestion && fecha_gestion !== 'None' && fecha_gestion !== '') {
        document.getElementById('view_fecha_gestion').textContent = formatFecha(fecha_gestion);
        gestionItem.style.display = 'block';
    } else {
        gestionItem.style.display = 'none';
    }

    // Observaciones
    const obsItem = document.getElementById('view_obs_item');
    if (observaciones && observaciones !== 'None' && observaciones !== '') {
        document.getElementById('view_observaciones').textContent = observaciones;
        obsItem.style.display = 'block';
    } else {
        obsItem.style.display = 'none';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function openManageModal(btn) {
    const modal = document.getElementById('manageModal');

    document.getElementById('manage_id').value = btn.dataset.id;
    document.getElementById('manage_palabra').textContent = btn.dataset.palabra;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(id) {
    const modal = document.getElementById(id);
    modal.classList.remove('active');
    document.body.style.overflow = '';

    // Detener video si es el viewModal
    if (id === 'viewModal') {
        const video = document.getElementById('view_video');
        video.pause();
        video.src = "";
    }
}

function toggleObs(estado) {
    const group = document.getElementById('obs_group');
    if (estado === 'rechazada') {
        group.querySelector('label').textContent = 'Motivo del Rechazo (Obligatorio)';
        group.querySelector('textarea').required = true;
    } else {
        group.querySelector('label').textContent = 'Observaciones (Opcional)';
        group.querySelector('textarea').required = false;
    }
}

// Cerrar modales con Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(m => closeModal(m.id));
    }
});
