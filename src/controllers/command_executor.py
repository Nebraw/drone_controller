from src.utils.logger import Logger
from src.utils.error_handler import catch_exceptions

class CommandExecutor:
    def __init__(self, tello):
        self.tello = tello
        self.logger = Logger()

    @catch_exceptions
    def execute_flight_sequence(self):
        self.logger.info("Décollage...")
        self.tello.takeoff()
        self.logger.info("Déplacement...")
        self.tello.move_left(100)
        self.tello.rotate_counter_clockwise(90)
        self.tello.move_forward(100)
        self.logger.info("Atterrissage...")
        self.tello.land()
