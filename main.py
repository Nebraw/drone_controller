from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
import cv2


if __name__ == "__main__":
    drone = DroneController()
    drone.connect()
    drone.getBattery()
    drone.streamon()

    agent = DroneAgent(drone)
    fsource = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("output.mp4", fsource, 30.0, (720,960))
    print("Drone activé !")
    try:
        while True:
            frame = drone.tello.get_frame_read().frame 
            if frame is not None:
                out.write(frame)
                print("Frame Witten")
                cv2.imshow("Tello Video Stream", frame)
            else:
                print("Frame vide reçue.")
            
            key_code = cv2.waitKey(1) & 0xFF
            
            if key_code != 255:
                key = chr(key_code)
                if agent.controleDrone(key) == 1:
                    break
    finally:
        drone.tello.streamoff()
        out.release()
        cv2.destroyAllWindows()
