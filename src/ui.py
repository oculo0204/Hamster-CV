import cv2
import os
import numpy as np

class UI:
    def __init__(self, image_folder="images"):
        self.images = {}
        for filename in os.listdir(image_folder):
            if filename.endswith(".jpg"):
                gesture_name = os.path.splitext(filename)[0].upper() # Use the name (without extension) as key
                path = os.path.join(image_folder, filename)
                img = cv2.imread(path)
                self.images[gesture_name] = img

    def show(self, frame, gesture):
        cv2.imshow("Camera", frame)
        if gesture in self.images:
            gesture_img = self.images[gesture]
            cv2.imshow("Hamster", gesture_img)
        else:
            cv2.imshow("Hamster", np.zeros((300, 300, 3), dtype=np.uint8))  # Show blank if no gesture