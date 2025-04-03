
from src.utils.error_handler import catch_exceptions

class CommandExecutor:
    def __init__(self, tello):
        self.tello = tello
    
    @catch_exceptions
    def execute_flight_sequence(self):
        print("Décollage...")
        self.tello.takeoff()
        print("Déplacement...")
        self.tello.move_left(100)
        self.tello.rotate_counter_clockwise(90)
        self.tello.move_forward(100)
        print("Atterrissage...")
        self.tello.land()
