"""
capturar_datos.py
─────────────────
Abre la webcam y guarda los landmarks (63 valores) de la mano
como archivos .npy en dataset/<clase>/.

USO:
  python capturar_datos.py hola
  python capturar_datos.py gracias

Controles:
  [ESPACIO] → guardar muestra
  [Q]       → salir
"""
import cv2
import mediapipe as mp
import numpy as np
import sys
import os

if len(sys.argv) < 2:
    print("Uso: python capturar_datos.py <clase>")
    print("Ejemplo: python capturar_datos.py hola")
    sys.exit(1)

clase = sys.argv[1]
ruta_clase = os.path.join(os.path.dirname(__file__), "..", "dataset", clase)
os.makedirs(ruta_clase, exist_ok=True)

# Contar muestras existentes para no sobreescribir
existentes = len([f for f in os.listdir(ruta_clase) if f.endswith(".npy")])
contador = existentes

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
print(f"\n📷 Capturando datos para: '{clase}'")
print(f"   Muestras existentes: {existentes}")
print(f"   [ESPACIO] = guardar | [Q] = salir\n")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    mano_detectada = False

    if resultado.multi_hand_landmarks:
        mano_detectada = True
        hand = resultado.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Info en pantalla
    color = (0, 255, 0) if mano_detectada else (0, 0, 255)
    estado = "MANO DETECTADA" if mano_detectada else "SIN MANO"
    cv2.putText(frame, f"Clase: {clase} | Muestras: {contador}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, estado, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Captura de Senas", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" ") and mano_detectada:
        puntos = resultado.multi_hand_landmarks[0].landmark
        landmarks = np.array([[p.x, p.y, p.z] for p in puntos]).flatten()  # (63,)

        archivo = os.path.join(ruta_clase, f"muestra_{contador:04d}.npy")
        np.save(archivo, landmarks)
        contador += 1
        print(f"   ✅ Guardada muestra #{contador} → {archivo}")

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n✅ Total muestras guardadas para '{clase}': {contador - existentes}")
print(f"   Total acumulado: {contador}")
