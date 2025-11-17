// Slider sidebar toggle - Version mejorada
if (!window.__sliderInitialized) {
  let toggle = null;
  let sidebar = null;
  let clickHandler = null;
  
  document.addEventListener('DOMContentLoaded', function () {
    toggle = document.querySelector('.sidebar-toggle');
    sidebar = document.querySelector('.sidebar');

    if (!toggle || !sidebar) return;

    // Restore previous state from localStorage (if set)
    try {
      const saved = localStorage.getItem('sidebar-collapsed');
      if (saved === 'true') {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        document.documentElement.classList.add('sidebar-collapsed');
      }
    } catch (err) {
      // ignore storage errors
    }

    const onToggle = function (e) {
      e.preventDefault();
      const isCollapsed = sidebar.classList.toggle('collapsed');
      document.body.classList.toggle('sidebar-collapsed', isCollapsed);
      document.documentElement.classList.toggle('sidebar-collapsed', isCollapsed);
      try { localStorage.setItem('sidebar-collapsed', isCollapsed ? 'true' : 'false'); } catch (err) {}
      toggle.setAttribute('aria-expanded', (!isCollapsed).toString());
    };

    // Remover listener anterior si existe
    if (window.__currentToggleHandler) {
      toggle.removeEventListener('click', window.__currentToggleHandler);
    }
    
    toggle.addEventListener('click', onToggle);
    window.__currentToggleHandler = onToggle;

    // Limpiar y recrear el click handler del document
    if (window.__documentClickHandler) {
      document.removeEventListener('click', window.__documentClickHandler);
    }

    clickHandler = function (e) {
      if (!sidebar || !toggle) return;
      if (sidebar.classList.contains('collapsed')) return;
      if (!sidebar.contains(e.target) && !toggle.contains(e.target) && window.innerWidth < 900) {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        document.documentElement.classList.add('sidebar-collapsed');
      }
    };

    document.addEventListener('click', clickHandler);
    window.__documentClickHandler = clickHandler;
  });

  window.__sliderInitialized = true;
}

// Función para limpiar todo cuando cambies de página
window.cleanupSlider = function() {
  if (window.__currentToggleHandler && toggle) {
    toggle.removeEventListener('click', window.__currentToggleHandler);
  }
  if (window.__documentClickHandler) {
    document.removeEventListener('click', window.__documentClickHandler);
  }
  window.__sliderInitialized = false;
  toggle = null;
  sidebar = null;
};