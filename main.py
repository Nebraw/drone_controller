from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import sys
import time
import platform
import threading
import cv2


def startVideoStream(tello, stopEvent):
    frame_read = tello.get_frame_read()
    while not stopEvent.is_set():
        frame = frame_read.frame
        print(frame is not None)
        if frame is not None:
          cv2.imshow("Tello Video", frame)


if platform.system() == "Windows":
    import msvcrt

    def get_key():
        """Lit une touche clavier sans attendre 'Entrée' (Windows)."""
        return msvcrt.getch().decode("utf-8").lower()

else:  # Linux/macOS
    import termios
    import tty

    def get_key():
        """Lit une touche clavier sans attendre 'Entrée' (Linux/macOS)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # Mode raw : capture immédiate
            key = sys.stdin.read(1)  # Lire un seul caractère
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restaurer
        return key.lower()

if __name__ == "__main__":
    drone = DroneController()
    agent = DroneAgent(drone.tello)

    drone.connect()

    past_actions = []
    reverse_action  = {
        "move_forward": "move_back",
        "move_left": "move_right",
        "move_up": "move_down",
        "rotate_cw": "rotate_ccw",
        "move_back": "move_forward",
        "move_right": "move_left",
        "move_down": "move_up",
        "rotate_ccw": "rotate_cw",
    }

    print("Mode autonome activé !")       
    try:
        while True:
            print("Your desires are my order:")
            key = get_key().lower()


            match key:
                case "w":
                    agent.execute_action("move_forward", 50)
                    past_actions.append("move_forward")
                case "s":
                    agent.execute_action("move_back", 50)
                    past_actions.append("move_back")
                case "a":
                    agent.execute_action("move_left", 50)
                    past_actions.append("move_left")
                case "d":
                    agent.execute_action("move_right", 50)
                    past_actions.append("move_right")
                case "r":
                    agent.execute_action("move_up", 50)
                    past_actions.append("move_up")
                case "f":
                    agent.execute_action("move_down", 50)
                    past_actions.append("move_down")
                case "q":
                    agent.execute_action("rotate_ccw", 45)
                    past_actions.append("rotate_ccw")
                case "e":
                    agent.execute_action("rotate_cw", 45)
                    past_actions.append("rotate_cw")
                case "t":
                    agent.execute_action("takeoff", 50)
                case "l":
                    drone.tello.land()
                case "m":
                    print(f"rewinding past actions: {past_actions}")
                    while len(past_actions) == 0:
                        back_action = reverse_action[past_actions.pop()]
                        back_value = 45 if back_action[0] == "r" else 50
                        print(f"rewind {back_action}, {back_value}")
                        agent.execute_action(back_action, back_value)
                        time.sleep(2)
                    drone.tello.land()
                case "x":
                    drone.tello.land()
                    print("end program.")
                    break
                case _: 
                    print("Unknown", key)
    finally:
        #stop_event.set()
        #video_thread.join()
        #drone.tello.streamoff()
        print("bye!")