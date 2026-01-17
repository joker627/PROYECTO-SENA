/**
 * Maneja las interacciones de la página de reportes.
 */

function openViewModal(btn) {
    const modal = document.getElementById('viewModal');

    // Datos del botón
    const id = btn.dataset.id;
    const desc = btn.dataset.descripcion;
    const usuario = btn.dataset.usuario;
    const fecha = btn.dataset.fecha;
    const estado = btn.dataset.estado;
    const prioridad = btn.dataset.prioridad;
    const tipo = btn.dataset.tipo;
    const evidencia = btn.dataset.evidencia;

    // Poblar modal texto
    document.getElementById('view_id').textContent = id;
    document.getElementById('view_descripcion').textContent = desc;
    document.getElementById('view_usuario').textContent = usuario || 'Anónimo';
    document.getElementById('view_fecha').textContent = fecha;
    document.getElementById('view_tipo').textContent = tipo || '-';

    // Manejo de Evidencia (Imagen o Video)
    const imgElement = document.getElementById('view_img_evidencia');
    const videoElement = document.getElementById('view_video_evidencia');
    const msgElement = document.getElementById('no_evidence_msg');

    // Reset
    imgElement.style.display = 'none';
    videoElement.style.display = 'none';
    msgElement.style.display = 'none';
    videoElement.pause();
    videoElement.src = "";
    imgElement.src = "";

    if (evidencia && evidencia !== 'None' && evidencia !== '') {
        let evSrc = evidencia;

        // Resolver ruta si es relativa
        if (!evSrc.startsWith('http') && !evSrc.startsWith('/static')) {
            evSrc = evSrc.startsWith('/') ? '/static' + evSrc : '/static/' + evSrc;
        }

        const ext = evSrc.split('.').pop().toLowerCase();
        const videoExtensions = ['mp4', 'webm', 'ogg', 'mov'];

        if (videoExtensions.includes(ext)) {
            videoElement.src = evSrc;
            videoElement.style.display = 'block';
            videoElement.load();
        } else {
            // Asumir que es imagen para el resto
            imgElement.src = evSrc;
            imgElement.style.display = 'block';
        }
    } else {
        msgElement.style.display = 'block';
    }

    // Prioridad Badge
    const priorityContainer = document.getElementById('view_prioridad_container');
    priorityContainer.innerHTML = `<span class="priority-badge ${prioridad}">${prioridad.charAt(0).toUpperCase() + prioridad.slice(1)}</span>`;

    // Estado Badge
    const statusContainer = document.getElementById('view_estado_container');
    statusContainer.innerHTML = `<span class="badge ${estado}">${estado.replace('_', ' ').charAt(0).toUpperCase() + estado.slice(1)}</span>`;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function openManageModal(btn) {
    const modal = document.getElementById('manageModal');

    document.getElementById('manage_id').value = btn.dataset.id;
    document.getElementById('manage_id_display').textContent = btn.dataset.id;
    document.getElementById('manage_estado').value = btn.dataset.estado;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(id) {
    const modal = document.getElementById(id);
    modal.classList.remove('active');
    document.body.style.overflow = '';

    // Detener video si existe
    if (id === 'viewModal') {
        const video = document.getElementById('view_video_evidencia');
        if (video) {
            video.pause();
            video.src = "";
        }
    }
}

// Cerrar con Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(m => closeModal(m.id));
    }
});
