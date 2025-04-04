import cv2

def test_webcam_video():
    # Ouvrir la première webcam (0 est généralement la webcam par défaut)
    cap = cv2.VideoCapture(0)

    # Vérifiez si la caméra a été ouverte correctement
    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la caméra.")
        return

    # Lire et afficher les frames de la webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture de la frame.")
            break

        cv2.imshow("Webcam Video Stream", frame)

        # Sortir de la boucle en appuyant sur la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_webcam_video()
