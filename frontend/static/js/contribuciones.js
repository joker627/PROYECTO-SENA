/**
 * Contribuciones - Optimizado
 */

const formatFecha = (f) => {
    if (!f || f === 'None') return '-';
    try { return new Date(f).toLocaleString('es-CO', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }); }
    catch { return f; }
};

function openViewModal(btn) {
    const d = btn.dataset;
    
    document.getElementById('view_avatar').textContent = d.usuario ? d.usuario[0].toUpperCase() : 'U';
    document.getElementById('view_palabra').textContent = d.palabra;
    document.getElementById('view_usuario').textContent = `Enviado por: ${d.usuario}`;
    document.getElementById('view_descripcion').textContent = d.descripcion;
    document.getElementById('view_fecha').textContent = formatFecha(d.fecha);

    // Video
    const video = document.getElementById('view_video');
    const section = video.closest('.view-video-section');
    
    if (d.video && d.video !== 'None') {
        let src = d.video;
        if (!src.startsWith('http') && !src.startsWith('/static')) {
            src = src.startsWith('/') ? '/static' + src : '/static/' + src;
        }
        video.src = src;
        section.style.display = 'flex';
        video.load();
    } else {
        section.style.display = 'none';
        video.src = '';
    }

    // Estado
    document.getElementById('view_estado_container').innerHTML = 
        `<span class="badge ${d.estado}">${d.estado.charAt(0).toUpperCase() + d.estado.slice(1)}</span>`;

    // Gestión
    const gestion = document.getElementById('view_gestion_item');
    if (d.fecha_gestion && d.fecha_gestion !== 'None') {
        document.getElementById('view_fecha_gestion').textContent = formatFecha(d.fecha_gestion);
        gestion.style.display = 'block';
    } else {
        gestion.style.display = 'none';
    }

    // Observaciones
    const obs = document.getElementById('view_obs_item');
    if (d.observaciones && d.observaciones !== 'None') {
        document.getElementById('view_observaciones').textContent = d.observaciones;
        obs.style.display = 'block';
    } else {
        obs.style.display = 'none';
    }

    SignTech.openModal('viewModal');
}

function openManageModal(btn) {
    document.getElementById('manage_id').value = btn.dataset.id;
    document.getElementById('manage_palabra').textContent = btn.dataset.palabra;
    SignTech.openModal('manageModal');
}

function closeModal(id) {
    SignTech.closeModal(id);
}

function toggleObs(estado) {
    const group = document.getElementById('obs_group');
    const isRechazada = estado === 'rechazada';
    group.querySelector('label').textContent = isRechazada ? 'Motivo del Rechazo (Obligatorio)' : 'Observaciones (Opcional)';
    group.querySelector('textarea').required = isRechazada;
}
