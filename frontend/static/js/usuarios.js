/**
 * Gestión de usuarios - Optimizado
 */

function openEditModal(btn) {
    const d = btn.dataset;
    document.getElementById('edit_id_usuario').value = d.id;
    document.getElementById('edit_nombre').value = d.nombre;
    document.getElementById('edit_correo').value = d.correo;
    document.getElementById('edit_rol').value = d.rol;
    document.getElementById('edit_estado').value = d.estado;
    SignTech.openModal('editUserModal');
}

function closeEditModal() { SignTech.closeModal('editUserModal'); }

function openViewModal(btn) {
    const d = btn.dataset;
    const inicial = d.nombre ? d.nombre[0].toUpperCase() : 'U';
    
    document.getElementById('view_avatar_circle').textContent = inicial;
    document.getElementById('view_nombre_title').textContent = d.nombre;
    document.getElementById('view_correo_subtitle').textContent = d.correo;
    document.getElementById('view_nombre').textContent = d.nombre;
    document.getElementById('view_correo').textContent = d.correo;
    document.getElementById('view_documento').textContent = d.documento;
    document.getElementById('view_rol').textContent = d.rol;
    document.getElementById('view_fecha').textContent = d.fecha;
    
    const estado = d.estado;
    document.getElementById('view_estado_container').innerHTML = 
        `<span class="badge ${estado}">${estado.charAt(0).toUpperCase() + estado.slice(1)}</span>`;
    
    SignTech.openModal('viewUserModal');
}

function closeViewModal() { SignTech.closeModal('viewUserModal'); }
function openCreateModal() { SignTech.openModal('createUserModal'); }
function closeCreateModal() { SignTech.closeModal('createUserModal'); }

// Cerrar modales al hacer clic fuera
window.onclick = (e) => {
    ['createUserModal', 'editUserModal', 'viewUserModal'].forEach(id => {
        if (e.target.id === id) SignTech.closeModal(id);
    });
};
