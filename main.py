from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import sys
import sys
import platform
import threading
import cv2
import time

def controleDrone(agent: DroneAgent, key:str):
    match key:
        case "w":
            agent.execute_action("move_forward", 50)
        case "s":
            agent.execute_action("move_back", 50)
        case "a":
            agent.execute_action("move_left", 50)
        case "d":
            agent.execute_action("move_right", 50)
        case "r":
            agent.execute_action("move_up", 50)
        case "f":
            agent.execute_action("move_down", 50)
        case "q":
            agent.execute_action("rotate_ccw", 45)
        case "e":
            agent.execute_action("rotate_cw", 45)
        case "t":
            agent.execute_action("takeoff")
        case "l":
            agent.execute_action("land")
        case "x":
            agent.execute_action("land")
            print("end program.")
            return 1
        case _: 
            print("Unknow", key)
    return 0

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
    drone.streamon()
    print("Mode autonome activé !")
    try:
        while True:
            frame = drone.tello.get_frame_read().frame  # Lire une frame du flux
            if frame is not None:
                cv2.imshow("Tello Video Stream", frame)  # Afficher la frame
            else:
                print("Frame vide reçue.")

            key = cv2.waitKey(1) & 0xFF
            print(chr(key))
            if controleDrone(agent, chr(key)) == 1:
                break
    finally:
        drone.tello.streamoff()
        cv2.destroyAllWindows()