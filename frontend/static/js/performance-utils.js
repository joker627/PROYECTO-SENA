// ===========================
// UTILIDADES DE PERFORMANCE - Debouncing y Throttling
// ===========================

/**
 * Debounce: Ejecuta una función solo después de que haya pasado un tiempo desde la última llamada
 * Útil para: búsquedas en tiempo real, resize de ventana, scroll events
 * 
 * @param {Function} func - Función a ejecutar
 * @param {Number} wait - Tiempo de espera en milisegundos
 * @returns {Function} Función debounced
 */
function debounce(func, wait = 300) {
    let timeout;
    
    return function executedFunction(...args) {
        const context = this;
        
        const later = () => {
            clearTimeout(timeout);
            func.apply(context, args);
        };
        
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle: Limita la ejecución de una función a una vez cada X milisegundos
 * Útil para: scroll infinito, drag events, mousemove
 * 
 * @param {Function} func - Función a ejecutar
 * @param {Number} limit - Tiempo mínimo entre ejecuciones en milisegundos
 * @returns {Function} Función throttled
 */
function throttle(func, limit = 300) {
    let inThrottle;
    let lastResult;
    
    return function executedFunction(...args) {
        const context = this;
        
        if (!inThrottle) {
            lastResult = func.apply(context, args);
            inThrottle = true;
            
            setTimeout(() => {
                inThrottle = false;
            }, limit);
        }
        
        return lastResult;
    };
}

/**
 * Request Animation Frame Throttle: Optimizado para animaciones
 * Limita ejecución al siguiente repaint del navegador
 * 
 * @param {Function} func - Función a ejecutar
 * @returns {Function} Función optimizada con RAF
 */
function rafThrottle(func) {
    let rafId = null;
    
    return function executedFunction(...args) {
        const context = this;
        
        if (rafId === null) {
            rafId = requestAnimationFrame(() => {
                func.apply(context, args);
                rafId = null;
            });
        }
    };
}

/**
 * Lazy Execution: Ejecuta función solo cuando el elemento es visible
 * Útil para: analytics, cargar contenido dinámico
 * 
 * @param {HTMLElement} element - Elemento a observar
 * @param {Function} callback - Función a ejecutar cuando sea visible
 * @param {Object} options - Opciones de IntersectionObserver
 */
function onVisible(element, callback, options = {}) {
    const defaultOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1,
        ...options
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, defaultOptions);
    
    observer.observe(element);
    
    return observer;
}

/**
 * Idle Callback: Ejecuta función cuando el navegador está inactivo
 * Útil para: tareas no críticas, analytics, prefetching
 * 
 * @param {Function} callback - Función a ejecutar
 * @param {Object} options - Opciones de timeout
 */
function onIdle(callback, options = {}) {
    const defaultOptions = {
        timeout: 2000, // Máximo 2 segundos de espera
        ...options
    };
    
    if ('requestIdleCallback' in window) {
        requestIdleCallback(callback, defaultOptions);
    } else {
        // Fallback para navegadores sin soporte
        setTimeout(callback, 1);
    }
}

/**
 * Memoize: Cachea resultados de funciones costosas
 * Útil para: cálculos complejos, búsquedas repetidas
 * 
 * @param {Function} func - Función a memoizar
 * @returns {Function} Función memoizada
 */
function memoize(func) {
    const cache = new Map();
    
    return function memoized(...args) {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            console.log('🎯 Cache hit:', key);
            return cache.get(key);
        }
        
        const result = func.apply(this, args);
        cache.set(key, result);
        
        return result;
    };
}

/**
 * Optimize Scroll: Mejora performance de scroll listeners
 * Combina RAF + throttle para scroll suave
 * 
 * @param {Function} callback - Función a ejecutar en scroll
 * @returns {Function} Listener optimizado
 */
function optimizeScroll(callback) {
    let ticking = false;
    
    return function optimizedScroll(event) {
        if (!ticking) {
            requestAnimationFrame(() => {
                callback(event);
                ticking = false;
            });
            
            ticking = true;
        }
    };
}

// ========== EXPORTAR FUNCIONES ==========
window.performanceUtils = {
    debounce,
    throttle,
    rafThrottle,
    onVisible,
    onIdle,
    memoize,
    optimizeScroll
};

// Hacer funciones disponibles globalmente
window.debounce = debounce;
window.throttle = throttle;
window.rafThrottle = rafThrottle;
window.onVisible = onVisible;
window.onIdle = onIdle;
window.memoize = memoize;
window.optimizeScroll = optimizeScroll;

console.log('✅ Performance Utils cargados correctamente');
