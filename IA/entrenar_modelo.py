"""
entrenar_modelo.py
──────────────────
Carga landmarks (.npy) de dataset/<clase>/ y entrena un modelo Keras
que se guarda como IA/modelo_senas.h5

USO:
  python entrenar_modelo.py

Estructura esperada:
  dataset/
    hola/
      muestra_0000.npy
      muestra_0001.npy
      ...
    gracias/
      muestra_0000.npy
      muestra_0001.npy
      ...
"""
import os
import numpy as np
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
MODELO_SALIDA = Path(__file__).resolve().parent / "modelo_senas.h5"

# ── Cargar datos ───────────────────────────────────────────────
CLASES = sorted([d for d in os.listdir(DATASET_DIR)
                 if os.path.isdir(DATASET_DIR / d)])

print(f" Clases encontradas: {CLASES}")

X, y = [], []

for idx, clase in enumerate(CLASES):
    ruta_clase = DATASET_DIR / clase
    archivos = [f for f in os.listdir(ruta_clase) if f.endswith(".npy")]
    print(f"   {clase}: {len(archivos)} muestras")

    if len(archivos) == 0:
        print(f"     Sin muestras para '{clase}'. Captura datos primero.")
        continue

    for archivo in archivos:
        landmarks = np.load(ruta_clase / archivo)
        X.append(landmarks)
        y.append(idx)

if len(X) == 0:
    print("\n No hay datos. Usa capturar_datos.py primero.")
    exit(1)

X = np.array(X)  # (n_muestras, 63)
y = np.array(y)

print(f"\n Total muestras: {len(X)}")
print(f"   Forma de X: {X.shape}")
print(f"   Clases: {dict(zip(CLASES, [int((y == i).sum()) for i in range(len(CLASES))]))}")

# ── Dividir datos ──────────────────────────────────────────────
from sklearn.model_selection import train_test_split  # noqa: E402

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n   Entrenamiento: {len(X_train)} | Test: {len(X_test)}")

# ── Construir modelo ──────────────────────────────────────────
from keras.models import Sequential  
from keras.layers import Dense, Dropout, BatchNormalization 
from keras.optimizers import Adam  
from keras.callbacks import EarlyStopping 

num_clases = len(CLASES)

modelo = Sequential([
    Dense(128, activation="relu", input_shape=(63,)),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation="relu"),
    BatchNormalization(),
    Dropout(0.3),

    Dense(32, activation="relu"),

    Dense(num_clases, activation="softmax")
])

modelo.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

modelo.summary()

# ── Entrenar ───────────────────────────────────────────────────
print("\n Entrenando modelo...\n")

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

historial = modelo.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stop],
    verbose=1
)

# ── Evaluar ────────────────────────────────────────────────────
loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
print(f"\n Resultado en test:")
print(f"   Loss:     {loss:.4f}")
print(f"   Accuracy: {accuracy:.4f} ({accuracy * 100:.1f}%)")

# ── Guardar ────────────────────────────────────────────────────
modelo.save(str(MODELO_SALIDA))
print(f"\n Modelo guardado en: {MODELO_SALIDA}")
print(f"   Clases (en orden): {CLASES}")
