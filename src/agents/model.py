import cv2
import numpy as np

class MLModel:
    def __init__(self, model_path="src/agents/model.h5"):
        self.action = 0 
        self.actions = ["takeoff", "move_forward", "rotate_left", "rotate_right", "land"]  # Classes possibles
           
    def predict(self, frame):
        """Prédit l'action à partir d'une image"""
        action=self.actions[self.action]
        self.action += 1
        return action