"""Servicio de IA: detección de lenguaje de señas con modelo Keras + MediaPipe."""
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import time
from pathlib import Path
from app.core.logger import logger

# ── MediaPipe (extrae landmarks) ──────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

# ── Modelo entrenado ──────────────────────────────────────────
# api/app/services/ia.py → parents[3] = api/ → parent = PROYECTO/
MODELO_PATH = Path(__file__).resolve().parents[3] / "IA" / "modelo_senas.h5"
CLASES = ["bien", "mal"]  # Orden alfabético (igual que el entrenamiento)

_modelo = None


def _cargar_modelo():
    """Carga el modelo Keras una sola vez (lazy singleton)."""
    global _modelo
    if _modelo is not None:
        return _modelo

    ruta = MODELO_PATH.resolve()
    if not ruta.exists():
        logger.error(f"Modelo no encontrado en: {ruta}")
        raise FileNotFoundError(f"Modelo no encontrado en: {ruta}")

    from keras.models import load_model  # noqa: E402
    _modelo = load_model(str(ruta))
    logger.info(f"Modelo de señas cargado desde: {ruta}")
    return _modelo


def _extraer_landmarks(frame) -> np.ndarray | None:
    """Extrae los 21 landmarks (63 valores) de un frame. Retorna None si no hay mano."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if not res.multi_hand_landmarks:
        return None

    puntos = res.multi_hand_landmarks[0].landmark
    # Aplanar a [x0, y0, z0, x1, y1, z1, ..., x20, y20, z20]
    return np.array([[p.x, p.y, p.z] for p in puntos]).flatten()


def predecir_sena(frame) -> str | None:
    """Predice la seña de un frame usando el modelo Keras."""
    landmarks = _extraer_landmarks(frame)
    if landmarks is None:
        return None

    modelo = _cargar_modelo()
    entrada = landmarks.reshape(1, -1)  # (1, 63)
    prediccion = modelo.predict(entrada, verbose=0)
    indice = int(np.argmax(prediccion))
    confianza = float(prediccion[0][indice])

    if confianza < 0.6:
        return None

    return CLASES[indice]


def traducir_video(video_bytes: bytes) -> dict:
    """Recibe bytes de un video y retorna la palabra detectada por el modelo."""
    ruta_video = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video_bytes)
            ruta_video = tmp.name

        cap = cv2.VideoCapture(ruta_video)

        if not cap.isOpened():
            logger.error("No se pudo abrir el video proporcionado")
            return {"palabra": "no_detectado"}

        conteo = {"bien": 0, "mal": 0}
        frames_analizados = 0

        while cap.isOpened() and frames_analizados < 30:
            ret, frame = cap.read()
            if not ret:
                break

            palabra = predecir_sena(frame)
            if palabra and palabra in conteo:
                conteo[palabra] += 1

            frames_analizados += 1

        cap.release()

        if frames_analizados == 0 or sum(conteo.values()) == 0:
            return {"palabra": "no_detectado"}

        resultado = max(conteo, key=conteo.get)
        logger.info(f"Seña detectada: '{resultado}'")

        return {"palabra": resultado}

    except FileNotFoundError as e:
        logger.error(str(e))
        return {"palabra": "modelo_no_encontrado"}

    except Exception as e:
        logger.error(f"Error al procesar video de señas: {e}")
        return {"palabra": "no_detectado"}

    finally:
        if ruta_video and os.path.exists(ruta_video):
            # Windows: cv2.VideoCapture puede tardar en liberar el archivo
            for _ in range(5):
                try:
                    os.remove(ruta_video)
                    break
                except PermissionError:
                    time.sleep(0.1)
