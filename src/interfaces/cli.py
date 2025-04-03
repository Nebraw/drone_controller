from src.controllers.drone_controller import DroneController

if __name__ == "__main__":
    drone = DroneController()
    
    while True:
        command = input("Commande (takeoff, land, exit): ").strip()
        if command == "takeoff":
            drone.executor.execute_flight_sequence()
        elif command == "land":
            drone.tello.land()
        elif command == "exit":
            break
        else:
            print("Commande inconnue.")
