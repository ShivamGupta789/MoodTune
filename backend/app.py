from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from PIL import Image
import io

from services.emotion_service import predict_emotion

app = FastAPI(title="MoodTune API")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MoodTune backend is running 🚀"}

@app.post("/detect-emotion")
async def detect_emotion(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        emotion = predict_emotion(image_cv)

        return {"emotion": emotion}

    except Exception as e:
        return {
            "error": "Failed to process image",
            "details": str(e)
        }
