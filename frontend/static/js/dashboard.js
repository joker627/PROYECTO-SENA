// dashboard.js - Limpio de lógica de datos.
// Se mantiene solo actualización de hora local y el botón de refrescar (que ahora recarga la página)

document.addEventListener('DOMContentLoaded', () => {
    // Actualizar fecha y hora
    updateDateTime();
    setInterval(updateDateTime, 60000);

    // Botón refrescar: recargar la página para traer nuevos datos del servidor
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshBtn.classList.add('loading');
            location.reload();
        });
    }
});

function updateDateTime() {
    const dateTimeElement = document.getElementById('currentDateTime');
    if (!dateTimeElement) return;

    const now = new Date();
    const options = {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
    };
    dateTimeElement.textContent = now.toLocaleDateString('es-CO', options);
}
