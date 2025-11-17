// performance-utils.js - Utilidades para optimización de rendimiento en frontend
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

// Throttle: Limita la ejecución de una función a intervalos regulares
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

// RAF Throttle: Usa requestAnimationFrame para optimizar llamadas frecuentes
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

// On Visible: Ejecuta función cuando el elemento es visible en viewport
// Útil para: lazy loading, animaciones al entrar en vista
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

// On Idle: Ejecuta función cuando el navegador está inactivo
// Útil para: tareas de baja prioridad, precarga de recursos
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

// Memoize: Cachea resultados de funciones puras para mejorar rendimiento
function memoize(func) {
    const cache = new Map();
    
    return function memoized(...args) {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            console.log(' Cache hit:', key);
            return cache.get(key);
        }
        
        const result = func.apply(this, args);
        cache.set(key, result);
        
        return result;
    };
}

// Optimize Scroll: Optimiza manejadores de scroll para evitar sobrecarga
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
(function (global) {
    const api = Object.freeze({
        debounce,
        throttle,
        rafThrottle,
        onVisible,
        onIdle,
        memoize,
        optimizeScroll
    });
    
// Evitar sobrescribir si ya existe
    if (!global.performanceUtils) {
        global.performanceUtils = api;
    } else {
        try {
            Object.assign(global.performanceUtils, api);
        } catch (e) {
            // Si falla la asignación, no hacemos nada para evitar sobrescribir
        }
    }

        // Soporte para CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = api;
    }
})(typeof window !== 'undefined' ? window : this);
