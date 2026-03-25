import cv2
import os
import numpy as np

class UI:
    def __init__(self, image_folder="images"):
        self.images = {}
        for filename in os.listdir(image_folder):
            if filename.endswith(".jpg"):
                gesture_name = os.path.splitext(filename)[0].upper()
                path = os.path.join(image_folder, filename)
                img = cv2.imread(path)
                if img is not None:
                    self.images[gesture_name] = img
        
        # 깜빡임 방지용 상태 변수
        self.current_gesture = None
        self.gesture_start_time = 0
        self.stable_duration = 10  # 10프레임 안정화 후 변경 (조절 가능)

    def show(self, frame, gesture):
        cv2.imshow("Camera", frame)
        
        # 제스처 안정화 로직
        if gesture and gesture != self.current_gesture:
            self.gesture_start_time += 1
            if self.gesture_start_time >= self.stable_duration:
                self.current_gesture = gesture
                self.gesture_start_time = 0  # 리셋
        elif gesture == self.current_gesture:
            self.gesture_start_time = 0  # 유지
        elif not gesture:
            self.current_gesture = None
            self.gesture_start_time = 0

        # 안정화된 제스처만 햄스터 표시
        if self.current_gesture and self.current_gesture in self.images:
            gesture_img = self.images[self.current_gesture]
            cv2.imshow("Hamster", gesture_img)
        else:
            # 검은 화면 대신 "No Gesture" 텍스트
            blank = np.zeros((300, 400, 3), dtype=np.uint8)
            cv2.putText(blank, "No Gesture", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("Hamster", blank)
