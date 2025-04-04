from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import sys
import sys
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
    drone.streamCamera()

    #stop_event = threading.Event()
    #video_thread = threading.Thread(target=startVideoStream, args=(drone.tello, stop_event))
    #video_thread.start()
    print("Mode autonome activé !")       
    try:
        while True:
            #frame = capture_frame(drone.tello)  # Récupère une image du drone
            #action = agent.analyze_frame()  # Analyse et prédit une action
            #agent.execute_action(action)  # Exécute l'action
            frame_read = drone.tello.get_frame_read()
            frame = frame_read.frame
            cv2.imshow("Tello Video", frame)
            key = get_key().lower()

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
                    drone.tello.land()
                case "x":
                    drone.tello.land()
                    print("end program.")
                    break
                case _: 
                    print("Unknow", key)
    finally:
        #stop_event.set()
        #video_thread.join()
        drone.tello.streamoff()
        cv2.destroyAllWindows()