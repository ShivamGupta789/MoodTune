import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# Absolute path to model (prevents reload issues)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "emotion_model.h5")

# Load model ONCE
model = load_model(MODEL_PATH, compile=False)

# FER2013 emotion labels (correct order for this model)
EMOTIONS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def predict_emotion(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(faces) == 0:
        return "No Face Detected"

    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]

    face = cv2.resize(face, (64, 64))
    face = face.astype("float32") / 255.0
    face = np.reshape(face, (1, 64, 64, 1))

    preds = model.predict(face, verbose=0)[0]

    emotion_index = int(np.argmax(preds))
    confidence = float(preds[emotion_index])

    return {
        "emotion": EMOTIONS[emotion_index],
        "confidence": round(confidence, 2)
    }
