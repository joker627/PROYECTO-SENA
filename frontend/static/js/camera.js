class Camera {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.stream = null;
        this.isRecording = false;
    }

    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: false
            });
            
            this.video.srcObject = this.stream;
            this.isRecording = true;
            
            this.video.onloadedmetadata = () => {
                this.canvas.width = this.video.videoWidth;
                this.canvas.height = this.video.videoHeight;
            };
            
            return true;
        } catch (error) {
            console.error('Error accediendo a la cámara:', error);
            alert('No se pudo acceder a la cámara. Asegúrate de dar los permisos necesarios.');
            return false;
        }
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.isRecording = false;
        }
    }

    captureFrame() {
        if (!this.isRecording) return null;
        
        this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        return this.canvas.toDataURL('image/jpeg');
    }
}

const camera = new Camera();

document.getElementById('startBtn').addEventListener('click', async () => {
    const started = await camera.start();
    if (started) {
        document.getElementById('startBtn').disabled = true;
        document.getElementById('translateBtn').disabled = false;
        document.getElementById('stopBtn').disabled = false;
    }
});

document.getElementById('stopBtn').addEventListener('click', () => {
    camera.stop();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('translateBtn').disabled = true;
    document.getElementById('stopBtn').disabled = true;
});
