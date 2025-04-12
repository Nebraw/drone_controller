from agents.drone_agent import DroneAgent
from unittest import MagicMock


def test_past_move():
     mockTello = MagicMock(spec=Tello)
     agent = DroneAgent()
     agent.execute_action("move_left")
     agent.execute_action("move_right")
     agent.execute_action("move_down")
     agent.execute_action("move_up")
     agent.execute_action("rotate_cw")



if __name__ == "__main__":
     test_past_move()