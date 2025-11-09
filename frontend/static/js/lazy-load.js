// ===========================
// LAZY LOADING - Carga diferida de videos e imágenes
// ===========================

document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
});

function initLazyLoading() {
    // Verificar soporte de IntersectionObserver
    if ('IntersectionObserver' in window) {
        initVideosLazyLoad();
        initImagesLazyLoad();
    } else {
        // Fallback: cargar todo inmediatamente si no hay soporte
        loadAllMediaImmediately();
    }
}

// ========== LAZY LOADING DE VIDEOS ==========
function initVideosLazyLoad() {
    const videos = document.querySelectorAll('video[data-lazy]');
    
    if (videos.length === 0) return;
    
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                const source = video.querySelector('source');
                
                if (source && source.dataset.src) {
                    // Cargar el video
                    source.src = source.dataset.src;
                    video.load();
                    video.removeAttribute('data-lazy');
                    
                    console.log('Video cargado:', source.src);
                    
                    // Dejar de observar este video
                    observer.unobserve(video);
                }
            }
        });
    }, {
        rootMargin: '200px', // Cargar 200px antes de entrar al viewport
        threshold: 0.1
    });
    
    videos.forEach(video => videoObserver.observe(video));
}

// ========== LAZY LOADING DE IMÁGENES ==========
function initImagesLazyLoad() {
    const images = document.querySelectorAll('img[data-lazy]');
    
    if (images.length === 0) return;
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                if (img.dataset.src) {
                    // Cargar la imagen
                    img.src = img.dataset.src;
                    
                    // Cargar srcset si existe
                    if (img.dataset.srcset) {
                        img.srcset = img.dataset.srcset;
                    }
                    
                    // Agregar clase cuando la imagen se haya cargado
                    img.addEventListener('load', () => {
                        img.classList.add('loaded');
                        console.log('Imagen cargada:', img.src);
                    });
                    
                    img.removeAttribute('data-lazy');
                    
                    // Dejar de observar esta imagen
                    observer.unobserve(img);
                }
            }
        });
    }, {
        rootMargin: '100px', // Cargar 100px antes de entrar al viewport
        threshold: 0.01
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ========== FALLBACK: CARGAR TODO INMEDIATAMENTE ==========
function loadAllMediaImmediately() {
    console.warn('IntersectionObserver no soportado. Cargando todo el contenido inmediatamente.');
    
    // Cargar todos los videos
    const videos = document.querySelectorAll('video[data-lazy]');
    videos.forEach(video => {
        const source = video.querySelector('source');
        if (source && source.dataset.src) {
            source.src = source.dataset.src;
            video.load();
            video.removeAttribute('data-lazy');
        }
    });
    
    // Cargar todas las imágenes
    const images = document.querySelectorAll('img[data-lazy]');
    images.forEach(img => {
        if (img.dataset.src) {
            img.src = img.dataset.src;
            if (img.dataset.srcset) {
                img.srcset = img.dataset.srcset;
            }
            img.removeAttribute('data-lazy');
        }
    });
}

// ========== UTILIDAD: PRELOAD DE VIDEOS CRÍTICOS ==========
function preloadCriticalVideo(videoElement) {
    // Para el hero video, se puede hacer preload inmediato
    const source = videoElement.querySelector('source');
    if (source && source.dataset.src) {
        source.src = source.dataset.src;
        videoElement.load();
        videoElement.removeAttribute('data-lazy');
    }
}

// Hacer función global por si se necesita llamar externamente
window.preloadCriticalVideo = preloadCriticalVideo;
