from djitellopy import Tello
import time
from src.utils.error_handler import catch_exceptions
from src.controllers.command_executor import CommandExecutor

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.executor = CommandExecutor(self.tello)

    @catch_exceptions
    def connect(self):
        print("Connexion au drone...")
        self.tello.connect()
        print(f"Batterie: {self.tello.get_battery()}%")

    @catch_exceptions
    def start(self):
        self.connect()
        self.executor.execute_flight_sequence()
