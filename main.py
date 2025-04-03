from src.controllers.drone_controller import DroneController
from src.agents.agent import DroneAgent
from src.agents.utils import capture_frame

if __name__ == "__main__":
    drone = DroneController()
    agent = DroneAgent(drone.tello)

    drone.connect()

    print("Mode autonome activé !")

    while True:
        frame = capture_frame(drone.tello)  # Récupère une image du drone
        action = agent.analyze_frame(frame)  # Analyse et prédit une action
        agent.execute_action(action)  # Exécute l'action

        key = input("Appuyez sur 'q' pour quitter : ")
        if key == 'q':
            drone.tello.land()
            break
