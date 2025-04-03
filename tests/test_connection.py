import unittest
from src.controllers.drone_controller import DroneController

class TestDroneConnection(unittest.TestCase):
    def test_connect(self):
        drone = DroneController()
        self.assertIsNone(drone.connect())

if __name__ == '__main__':
    unittest.main()
