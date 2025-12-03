import cv2
import mediapipe as mp

from src.camera import Camera
from src.detector import Detector
from src.ui import UI

camera = Camera()
detector = Detector()
ui = UI(image_folder="images")

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    # Detect hands and landmarks
    frame = detector.find_hands(frame, draw=True)
    gesture = detector.detect_gesture()

    ui.show(frame, gesture)

    # cv2.imshow("Webcam", frame) # Show a window with the webcam feed

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()