// ===========================
// UTILIDADES DE PERFORMANCE 
// ===========================

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

console.log(' Performance Utils cargados correctamente');
