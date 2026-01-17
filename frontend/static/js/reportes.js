/**
 * Reportes - Optimizado
 */

function openViewModal(btn) {
    const d = btn.dataset;
    
    document.getElementById('view_id').textContent = d.id;
    document.getElementById('view_descripcion').textContent = d.descripcion;
    document.getElementById('view_usuario').textContent = d.usuario || 'Anónimo';
    document.getElementById('view_fecha').textContent = d.fecha;
    document.getElementById('view_tipo').textContent = d.tipo || '-';

    // Evidencia
    const img = document.getElementById('view_img_evidencia');
    const video = document.getElementById('view_video_evidencia');
    const msg = document.getElementById('no_evidence_msg');
    
    img.style.display = video.style.display = msg.style.display = 'none';
    video.pause(); video.src = ''; img.src = '';

    if (d.evidencia && d.evidencia !== 'None') {
        let src = d.evidencia;
        if (!src.startsWith('http') && !src.startsWith('/static')) {
            src = src.startsWith('/') ? '/static' + src : '/static/' + src;
        }
        
        const ext = src.split('.').pop().toLowerCase();
        if (['mp4', 'webm', 'ogg', 'mov'].includes(ext)) {
            video.src = src;
            video.style.display = 'block';
            video.load();
        } else {
            img.src = src;
            img.style.display = 'block';
        }
    } else {
        msg.style.display = 'block';
    }

    // Badges
    document.getElementById('view_prioridad_container').innerHTML = 
        `<span class="priority-badge ${d.prioridad}">${d.prioridad.charAt(0).toUpperCase() + d.prioridad.slice(1)}</span>`;
    document.getElementById('view_estado_container').innerHTML = 
        `<span class="badge ${d.estado}">${d.estado.replace('_', ' ').charAt(0).toUpperCase() + d.estado.slice(1)}</span>`;

    SignTech.openModal('viewModal');
}

function openManageModal(btn) {
    document.getElementById('manage_id').value = btn.dataset.id;
    document.getElementById('manage_id_display').textContent = btn.dataset.id;
    document.getElementById('manage_estado').value = btn.dataset.estado;
    SignTech.openModal('manageModal');
}

function closeModal(id) {
    SignTech.closeModal(id);
}
