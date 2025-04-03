import cv2
import numpy as np
from tensorflow.keras.models import load_model

class MLModel:
    def __init__(self, model_path="src/agents/model.h5"):
        self.model = load_model(model_path)

    def preprocess_image(self, frame):
        """Prétraitement d'une image pour le modèle (mise à l'échelle, conversion, etc.)"""
        frame = cv2.resize(frame, (64, 64))  # Taille attendue par le modèle
        frame = frame / 255.0  # Normalisation
        frame = np.expand_dims(frame, axis=0)  # Ajout d'une dimension batch
        return frame

    def predict(self, frame):
        """Prédit l'action à partir d'une image"""
        processed_frame = self.preprocess_image(frame)
        prediction = self.model.predict(processed_frame)
        classes = ["move_forward", "rotate_left", "land"]  # Classes possibles
        return classes[np.argmax(prediction)]
