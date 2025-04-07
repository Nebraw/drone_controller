from src.agents.model import MLModel
from djitellopy import Tello
from collections import deque 

class DroneAgent:
    def __init__(self, tello:Tello):
        self.tello:Tello = tello
        self.model = MLModel()
        self.pastactions = deque()


    def analyze_frame(self,frame=None):
        """Analyse une image et retourne une action"""
        action = self.model.predict(frame)
        print(f"Action recommandée par le modèle : {action}")
        return action

    def execute_action(self, action, value=None, isMirror = False):
        """Exécute une action sur le drone en fonction de la prédiction du modèle"""
        try:
            print(f"Executing action  {action} mirror : {isMirror}")
            
            match action:
                case "takeoff":
                    self.tello.takeoff() 
                case "land":
                    self.tello.land()
                case "move_forward":
                    self.tello.move_forward(value or 50)
                case "move_back":
                    self.tello.move_back(value or 50)
                case "move_left":
                    self.tello.move_left(value or 50)
                case "move_right":
                    self.tello.move_right(value or 50)
                case "move_up":
                    self.tello.move_up(value or 50)
                case "move_down":
                    self.tello.move_down(value or 50)
                case "rotate_cw":
                    self.tello.rotate_clockwise(value or 90)
                case "rotate_ccw":
                    self.tello.rotate_counter_clockwise(value or 90)
                case "battery":
                    print(f"Battery: {self.tello.get_battery()}%")
                case "speed":
                    print(f"Speed: {self.tello.get_speed()} cm/s")
                case _:
                    print(f"Action unknown: {action}")
            
            if not isMirror:
                self.pastactions.append(action)
        
        except Exception as e:
            print(f"Failed to execute {action}: {e}")
    
    def hasLastAction(self):
        return len(self.pastactions) > 0
        
    
    def get_mirror_move_of_last_position(self):
        if (len(self.pastactions) == 0):
            print("Drone is already at initial position")
            return None

        else:
            return self.pastactions.pop()
        
            