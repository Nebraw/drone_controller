from src.agents.model import MLModel
from src.utils.logger import Logger

class DroneAgent:
    def __init__(self, tello):
        self.tello = tello
        self.model = MLModel()
        self.logger = Logger()

    def analyze_frame(self, frame):
        """Analyse une image et retourne une action"""
        action = self.model.predict(frame)
        self.logger.info(f"Action recommandée par le modèle : {action}")
        return action

    def execute_action(self, action):
        """Exécute une action sur le drone en fonction de la prédiction du modèle"""
        if action == "move_forward":
            self.tello.move_forward(50)
        elif action == "rotate_left":
            self.tello.rotate_counter_clockwise(45)
        elif action == "land":
            self.tello.land()
        else:
            self.logger.info("Aucune action reconnue.")
