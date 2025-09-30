// Funcionalidad común para switching de modos (señas/texto)
function initModeSwitch() {
    function setActive(el) {
        const els = document.querySelectorAll('.translation-actions .action-btn, .action-btn');
        els.forEach(e => e.classList.remove('active'));
        if (el) el.classList.add('active');
    }

    // Determinar modo activo basado en la URL
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('/texto')) {
        const textBtn = document.getElementById('mode-text-to-sign');
        setActive(textBtn);
    } else if (currentPath.includes('/senas')) {
        const signBtn = document.getElementById('mode-sign-to-text');
        setActive(signBtn);
    }

    // Event listeners para los botones
    const signBtn = document.getElementById('mode-sign-to-text');
    const textBtn = document.getElementById('mode-text-to-sign');

    if (signBtn) {
        signBtn.addEventListener('click', () => setActive(signBtn));
    }

    if (textBtn) {
        textBtn.addEventListener('click', (e) => {
            setActive(textBtn);
            // Permitir navegación por defecto si es un enlace
        });
    }
}

// Funcionalidad para cámara (reutilizable)
function initCameraControls() {
    const video = document.getElementById('camera');
    const startBtn = document.getElementById('start-camera');
    const stopBtn = document.getElementById('stop-camera');
    
    if (!video || !startBtn || !stopBtn) return;

    let currentStream = null;

    async function startCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'user' }, 
                audio: false 
            });
            currentStream = stream;
            video.srcObject = stream;
            startBtn.textContent = 'En curso';
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } catch (err) {
            console.warn('No se pudo acceder a la cámara', err);
            const translationText = document.getElementById('translation-text');
            if (translationText) {
                translationText.textContent = 'No se pudo acceder a la cámara. Por favor permita el acceso o use un dispositivo con cámara.';
            }
            startBtn.textContent = 'Reintentar';
            startBtn.disabled = false;
        }
    }

    function stopCamera() {
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
            currentStream = null;
        }
        video.srcObject = null;
        startBtn.textContent = 'Iniciar';
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }

    startBtn.addEventListener('click', function () {
        startBtn.disabled = true;
        startBtn.textContent = 'Solicitando...';
        startCamera();
    });

    stopBtn.addEventListener('click', stopCamera);

    // Estado inicial
    stopBtn.disabled = true;

    // Auto-start si el permiso ya está concedido
    if (navigator.permissions) {
        navigator.permissions.query({ name: 'camera' }).then(function (perm) {
            if (perm.state === 'granted') startCamera();
        }).catch(() => {});
    }
}

// Funcionalidad para traducción de texto (reutilizable)
function initTextTranslation() {
    const translateBtn = document.getElementById('translate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const input = document.getElementById('input-text');
    const result = document.getElementById('result-text');

    if (!translateBtn || !clearBtn || !input || !result) return;

    translateBtn.addEventListener('click', function () {
        const text = input.value.trim();
        if (!text) {
            result.textContent = 'Escribe algo para traducir.';
            return;
        }
        // Comportamiento de traducción simulado: invertir palabras como placeholder
        const translated = text.split(' ').reverse().join(' ');
        result.textContent = translated;
    });

    clearBtn.addEventListener('click', function () {
        input.value = '';
        result.textContent = 'Resultado aparecerá aquí';
    });
}

// Inicializar todas las funcionalidades cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    initModeSwitch();
    initCameraControls();
    initTextTranslation();
});