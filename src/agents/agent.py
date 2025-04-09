from typing import Tuple
from ..controllers.drone_controller import DroneController
from src.agents.model import MLModel
import threading

class DroneAgent:
    def __init__(self, droneController: DroneController = DroneController(1)):
        self.model = MLModel()
        self.drone = droneController
        self.treahd:threading = threading

    def analyze_frame(self,frame=None):
        """Analyse une image et retourne une action"""
        action = self.model.predict(frame)
        print(f"Action recommandée par le modèle : {action}")
        return action

    def controleDrone(self,key:str):
        def action():
            match key:
                case "w":
                    self.drone.execute_action("forward", 50)
                case "s":
                    self.drone.execute_action("back", 50)
                case "a":
                    self.drone.execute_action("left", 50)
                case "d":
                    self.drone.execute_action("right", 50)
                case "r":
                    self.drone.execute_action("up", 50)
                case "f":
                    self.drone.execute_action("down", 50)
                case "q":
                    self.drone.execute_action("rotate_ccw", 45)
                case "e":
                    self.drone.execute_action("rotate_cw", 45)
                case "t":
                    self.drone.execute_action("takeoff")
                case "b":
                    self.drone.execute_action("battery")
                case "l":
                    self.drone.execute_action("land")
                case "p":
                    self.drone.execute_action("backToBase")
                case "x":
                    self.drone.execute_action("land")
                    print("end program.")

        print("Battery:", self.drone.getBattery())
        print("XYZ:", self.drone.get_acceleration_xyz())
        print("Barometre:", self.drone.getBarometre())
        print("Height, Altitude", self.drone.getHeight(), self.drone.getAltitude())

        if key == "x":
            action()
            return 1
        else:
            threading.Thread(target = action).start()
            return 0