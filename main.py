import threading
from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import cv2

def controleDrone(drone: DroneController, key:str):
    def action():
        match key:
            case "w":
                drone.execute_action("move_forward", 50)
            case "s":
                drone.execute_action("move_back", 50)
            case "a":
                drone.execute_action("move_left", 50)
            case "d":
                drone.execute_action("move_right", 50)
            case "r":
                drone.execute_action("move_up", 50)
            case "f":
                drone.execute_action("move_down", 50)
            case "q":
                drone.execute_action("rotate_ccw", 45)
            case "e":
                drone.execute_action("rotate_cw", 45)
            case "t":
                drone.execute_action("takeoff")
            case "b":
                drone.execute_action("battery")
            case "l":
                drone.execute_action("land")
            case "p":
                drone.execute_action("backToBase")
            case "x":
                drone.execute_action("land")
                print("end program.")

    print("Battery:", drone.getBattery())
    print("XYZ:", drone.get_acceleration_xyz())
    print("Barometre:", drone.getBarometre())
    print("Height, Altitude", drone.getHeight(), drone.getAltitude())
    
    if key == "x":
        action()
        return 1
    else:
        threading.Thread(target = action).start()
        return 0

if __name__ == "__main__":
    drone = DroneController()
    agent = DroneAgent(drone.tello)

    drone.connect()
    drone.getBattery()
    drone.streamon()
    fsource = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter("output.avi", fsource, 20.0, (720,960))
    print("Mode autonome activé !")
    try:
        while True:
            frame = drone.tello.get_frame_read().frame  # Lire une frame du flux
            if frame is not None:
                out.write(frame)
                cv2.imshow("Tello Video Stream", frame)  # Afficher la frame
            else:
                print("Frame vide reçue.")
            
            key_code = cv2.waitKey(1) & 0xFF
            
            if key_code != 255:  # Aucune touche pressée
                key = chr(key_code)
                if controleDrone(drone, key) == 1:
                    break
    finally:
        drone.tello.streamoff()
        out.release()
        cv2.destroyAllWindows()
