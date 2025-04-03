from djitellopy import Tello
import time
from src.utils.logger import Logger
from src.utils.error_handler import catch_exceptions
from src.controllers.command_executor import CommandExecutor

class DroneController:
    def __init__(self):
        self.tello = Tello()
        self.logger = Logger()
        self.executor = CommandExecutor(self.tello)

    @catch_exceptions
    def connect(self):
        self.logger.info("Connexion au drone...")
        self.tello.connect()
        self.logger.info(f"Batterie: {self.tello.get_battery()}%")

    @catch_exceptions
    def start(self):
        self.connect()
        self.executor.execute_flight_sequence()
