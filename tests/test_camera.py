import cv2

def test_webcam_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la caméra.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture de la frame.")
            break

        cv2.imshow("Webcam Video Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_webcam_video()
