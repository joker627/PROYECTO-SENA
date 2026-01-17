/**
 * Dashboard - Optimizado
 */
document.addEventListener('DOMContentLoaded', () => {
    // Actualizar fecha/hora
    const dt = document.getElementById('currentDateTime');
    if (dt) {
        const update = () => dt.textContent = new Date().toLocaleDateString('es-CO', {
            weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
        });
        update();
        setInterval(update, 60000);
    }

    // Botón refrescar
    const btn = document.getElementById('refreshBtn');
    if (btn) btn.onclick = () => { btn.classList.add('loading'); location.reload(); };
});
