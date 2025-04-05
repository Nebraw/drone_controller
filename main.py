import threading
from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import cv2
import asyncio

def controleDrone(agent: DroneAgent, key:str):
    def action():
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
            case "b":
                agent.execute_action("battery")
            case "l":
                agent.execute_action("land")
            case "x":
                agent.execute_action("land")
                print("end program.")
    if key == "x":
        action()
        return 1
    else:
        threading.Thread(target=action).start()
        return 0

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
            key_code = cv2.waitKey(1) & 0xFF
            if key_code != 255:  # Aucune touche pressée
                key = chr(key_code)
                if controleDrone(agent, key) == 1:
                    break
    finally:
        drone.tello.streamoff()
        cv2.destroyAllWindows()