/**
 * Gestión interactiva de la página de usuarios.
 * Maneja la apertura y cierre de modales y la precarga de datos para edición.
 */

/**
 * Abre el modal de edición y precarga los campos con la información del elemento.
 * @param {HTMLElement} btn - Botón que disparó el evento.
 */
function openEditModal(btn) {
    const modal = document.getElementById('editUserModal');

    // Asignar valores desde los atributos data del botón
    document.getElementById('edit_id_usuario').value = btn.dataset.id;
    document.getElementById('edit_nombre').value = btn.dataset.nombre;
    document.getElementById('edit_correo').value = btn.dataset.correo;
    document.getElementById('edit_rol').value = btn.dataset.rol;
    document.getElementById('edit_estado').value = btn.dataset.estado;

    // Activar el modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Evitar scroll al estar el modal abierto
}

/**
 * Cierra el modal de edición de usuario.
 */
function closeEditModal() {
    const modal = document.getElementById('editUserModal');
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Restaurar scroll
}

/**
 * Abre el modal de visualización de datos de usuario (solo lectura).
 * @param {HTMLElement} btn - Botón que disparó el evento.
 */
function openViewModal(btn) {
    const modal = document.getElementById('viewUserModal');

    // Información principal
    const nombre = btn.dataset.nombre;
    const correo = btn.dataset.correo;
    const inicial = nombre ? nombre.split(' ')[0][0].toUpperCase() : 'U';

    document.getElementById('view_avatar_circle').textContent = inicial;
    document.getElementById('view_nombre_title').textContent = nombre;
    document.getElementById('view_correo_subtitle').textContent = correo;

    // Grid de detalles
    document.getElementById('view_nombre').textContent = nombre;
    document.getElementById('view_correo').textContent = correo;
    document.getElementById('view_documento').textContent = btn.dataset.documento;
    document.getElementById('view_rol').textContent = btn.dataset.rol;
    document.getElementById('view_fecha').textContent = btn.dataset.fecha;

    // Badge de estado dinámico
    const estado = btn.dataset.estado;
    const estadoContainer = document.getElementById('view_estado_container');
    const estadoLabel = estado.charAt(0).toUpperCase() + estado.slice(1);
    estadoContainer.innerHTML = `<span class="badge ${estado}">${estadoLabel}</span>`;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}


/**
 * Cierra el modal de visualización.
 */
function closeViewModal() {
    const modal = document.getElementById('viewUserModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Abre el modal de creación de nuevo usuario.
 */
function openCreateModal() {
    const modal = document.getElementById('createUserModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Cierra el modal de creación.
 */
function closeCreateModal() {
    const modal = document.getElementById('createUserModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Cierre de modales al hacer clic fuera del contenido
window.addEventListener('click', (event) => {
    const createModal = document.getElementById('createUserModal');
    const editModal = document.getElementById('editUserModal');
    const viewModal = document.getElementById('viewUserModal');

    if (event.target === createModal) {
        closeCreateModal();
    }
    if (event.target === editModal) {
        closeEditModal();
    }
    if (event.target === viewModal) {
        closeViewModal();
    }
});

// Cierre de modales con la tecla Escape
window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeCreateModal();
        closeEditModal();
        closeViewModal();
    }
});
