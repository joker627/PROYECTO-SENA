// Solicitudes - UI: modales y animaciones

document.addEventListener('DOMContentLoaded', function() {
    // Las alertas flash se convierten a toasts automáticamente por toast.js
    initModalHandlers();
});

// Manejadores de modales
function initModalHandlers() {
    document.querySelectorAll('.btn-reject').forEach(button => {
        button.addEventListener('click', function() {
            const idSolicitud = this.getAttribute('data-id');
            const nombreSolicitante = this.getAttribute('data-nombre');
            openRejectModal(idSolicitud, nombreSolicitante);
        });
    });
}

function openRejectModal(idSolicitud, nombreSolicitante) {
    const modal = document.getElementById('rejectModal');
    if (modal) {
        modal.style.display = 'flex';
        document.getElementById('solicitanteNombre').textContent = nombreSolicitante;
        document.getElementById('rejectForm').action = `/solicitudes/rechazar/${idSolicitud}`;
    }
}

function closeRejectModal() {
    const modal = document.getElementById('rejectModal');
    if (modal) {
        modal.style.display = 'none';
        document.getElementById('rejectForm').reset();
    }
}

// Cerrar modal al hacer clic fuera
window.addEventListener('click', function(event) {
    const rejectModal = document.getElementById('rejectModal');
    if (event.target === rejectModal) {
        closeRejectModal();
    }
});
