from typing import Tuple
from djitellopy import Tello
import time
from src.utils.error_handler import catch_exceptions
from src.controllers.command_executor import CommandExecutor

class DroneController:
    def __init__(self, number_retry:int= 1):
        self.tello = Tello()
        self.tello.retry_count = number_retry
        self.executor = CommandExecutor(self.tello)
        self.backToBase = False
        self.backActions = []
        self.actions = []

        self.mirror = {
            "takeoff":"land",
            "land":"takeoff",
            "forward":"back",
            "back":"forward",
            "right":"left",
            "left":"right",
            "up":"down",
            "down":"up",
            "rotate_cw":"rotate_ccw",
            "rotate_ccw":"rotate_cw"
        }


    @catch_exceptions
    def connect(self):
        print("Connection to the drone...")
        self.tello.connect()
        
    def getBattery(self):
         print(f"Battery: {self.tello.get_battery()}%")

    @catch_exceptions
    def streamon(self):
        self.tello.streamon()
        time.sleep(2)
        print('Camera Started')        
    
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


    def execute_action(self, action, value=20, backToBase=False):
        success:bool = False
        try:
            match action:
                case "takeoff":
                    success = self.tello.send_control_command(action, timeout=Tello.TAKEOFF_TIMEOUT) 
                case "land":
                    self.tello.land()
                case "forward":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "back":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "left":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "right":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "up":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "down":
                     success = self.tello.send_control_command("{} {}".format(action, value))
                case "rotate_cw":
                     success = self.tello.send_control_command("cw {}".format(value))
                case "rotate_ccw":
                     success = self.tello.send_control_command("ccw {}".format(value))
                case "battery":
                    print(f"Battery: {self.tello.get_battery()}%")
                case "backToBase":
                    self.modeBackToBase()
                    return
                case _:
                    print(f"Action unknown: {action}")
            
            print(success)
            if success and not backToBase:
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