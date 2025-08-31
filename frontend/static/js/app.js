class App {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('translateBtn').addEventListener('click', () => {
            this.translate();
        });

        document.getElementById('submitFeedback').addEventListener('click', () => {
            this.submitFeedback();
        });
    }

    async translate() {
        try {
            const frameData = camera.captureFrame();
            if (!frameData) {
                alert('Primero inicia la cámara');
                return;
            }

            document.getElementById('translationResult').innerHTML = '<p>Procesando...</p>';

            const response = await fetch(\\/api/translate\, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ video_data: frameData })
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('translationResult').innerHTML = \
                    <p><strong>Texto:</strong> \</p>
                    <p><strong>Confianza:</strong> \%</p>
                \;
                document.querySelector('.feedback').style.display = 'block';
            } else {
                document.getElementById('translationResult').innerHTML = \
                    <p class="error">Error: \</p>
                \;
            }
        } catch (error) {
            console.error('Error en traducción:', error);
            document.getElementById('translationResult').innerHTML = \
                <p class="error">Error de conexión con el servidor</p>
            \;
        }
    }

    async submitFeedback() {
        try {
            const correction = document.getElementById('correctionInput').value;
            if (!correction) {
                alert('Por favor ingresa una corrección');
                return;
            }

            const response = await fetch(\\/api/feedback\, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    original: document.getElementById('translationResult').textContent,
                    correction: correction
                })
            });

            const result = await response.json();

            if (result.success) {
                alert('¡Gracias por tu feedback!');
                document.getElementById('correctionInput').value = '';
                document.querySelector('.feedback').style.display = 'none';
            } else {
                alert('Error enviando feedback: ' + result.error);
            }
        } catch (error) {
            console.error('Error enviando feedback:', error);
            alert('Error de conexión');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
