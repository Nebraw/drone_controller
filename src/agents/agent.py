from typing import Tuple
from src.agents.model import MLModel
from djitellopy import Tello
from collections import deque 

class DroneAgent:
    def __init__(self, tello:Tello):
        self.tello:Tello = tello
        self.model = MLModel()


    def analyze_frame(self,frame=None):
        """Analyse une image et retourne une action"""
        action = self.model.predict(frame)
        print(f"Action recommandée par le modèle : {action}")
        return action

    