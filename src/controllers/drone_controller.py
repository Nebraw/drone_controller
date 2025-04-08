from typing import Tuple
from djitellopy import Tello
import time
from src.utils.error_handler import catch_exceptions
from src.controllers.command_executor import CommandExecutor

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.tello.retry_count = 1
        self.executor = CommandExecutor(self.tello)
        self.backToBase = False
        self.backActions = []
        self.actions = []

        self.mirror = {
            "takeoff":"land",
            "land":"takeoff",
            "move_forward":"move_back",
            "move_back":"move_forward",
            "move_right":"move_left",
            "move_left":"move_right",
            "move_up":"move_down",
            "move_down":"move_up",
            "rotate_cw":"rotate_ccw",
            "rotate_ccw":"rotate_cw"
        }


    @catch_exceptions
    def connect(self):
        print("Connexion au drone...")
        self.tello.connect()
        print(f"Batterie: {self.tello.get_battery()}%")

    def getBattery(self):
         print(f"Battery: {self.tello.get_battery()}%")

    @catch_exceptions
    def streamon(self):
        print('lancement de camera')
        self.tello.streamon()
        time.sleep(2)
        print('camera lancé')
        
    @catch_exceptions
    def getframe(self):
        return self.tello.get_frame_read()
    
    @catch_exceptions
    def start(self):
        self.connect()
        self.executor.execute_flight_sequence()

    def addAction(self, action, value=None):
        print("Add Action", action, value)
        if len(self.backActions) == 0:
            self.backActions.append((action, value))
        else:
            last_action, last_value = self.backActions[-1]
            if last_action == action:
                self.backActions[-1] = (action, last_value + value)
            else:
                self.backActions.append((action, value))


    def execute_action(self, action, value=None, backToBase=False):
        """Exécute une action sur le drone en fonction de la prédiction du modèle"""
        try:
            match action:
                case "takeoff":
                    self.tello.takeoff() 
                case "land":
                    self.tello.land()
                case "move_forward":
                    self.tello.move_forward(value)
                case "move_back":
                    self.tello.move_back(value)
                case "move_left":
                    self.tello.move_left(value)
                case "move_right":
                    self.tello.move_right(value)
                case "move_up":
                    self.tello.move_up(value)
                case "move_down":
                    self.tello.move_down(value)
                case "rotate_cw":
                    self.tello.rotate_clockwise(value)
                case "rotate_ccw":
                    self.tello.rotate_counter_clockwise(value)
                case "battery":
                    print(f"Battery: {self.tello.get_battery()}%")
                case "speed":
                    print(f"Speed: {self.tello.get_speed()} cm/s")
                case "backToBase":
                    self.modeBackToBase()
                    return
                case _:
                    print(f"Action unknown: {action}")
            if not backToBase:
                self.actions.append((action,value))
                self.addAction(self.mirror[action], value)             
        except Exception as e:
            print(f"Failed to execute {action}: {e}")

    def modeBackToBase(self):
        print("execute backToBase", self.backActions)
        while(len(self.backActions) > 0):
            action,value = self.backActions.pop(-1)
            print(action, value)
            self.execute_action(action, value, True)
            time.sleep(1)

    def getHeight(self)-> int:
        return self.tello.get_height()
    
    def getAltitude(self)-> int:
        return self.tello.query_attitude()

    def getBarometre(self) -> int:
        return self.tello.get_barometer()
    
    def get_acceleration_xyz(self) -> Tuple[int, int, int]:
        return (self.tello.get_acceleration_x(),self.tello.get_acceleration_y(),self.tello.get_acceleration_z())