import cv2

def capture_frame(tello):
    """Capture une image depuis la caméra du drone"""
    frame = tello.get_frame_read().frame
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
