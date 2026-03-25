import mediapipe as mp
import cv2

class Detector:
    def __init__(self, max_hands=2, detection_confidence=0.5, tracking_confidence=0.85):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,  # 손 검출 민감도 ↑
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        """Detect hands and optionally draw landmarks"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_landmarks(self):
        """Returns list of landmark positions (x, y) for the first detected hand"""
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand.landmark):
                lm_list.append((lm.x, lm.y))
        return lm_list

    def is_right_hand(self):
        """손이 오른손인지 확인 (MediaPipe handedness 사용)"""
        if self.results.multi_handedness:
            handedness = self.results.multi_handedness[0].classification[0].label
            return handedness == "Right"
        return True  # 기본값 오른손

    def fingers_up(self):
        """
        Returns a list of 5 elements (1 for up, 0 for down)
        Thumb, Index, Middle, Ring, Pinky
        """
        lm_list = self.get_landmarks()
        if not lm_list or len(lm_list) < 21:
            return []

        fingers = []
        is_right = self.is_right_hand()

        # 엄지 (왼손/오른손 구분)
        if is_right:
            # 오른손: 엄지 x > 3번 x
            fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)
        else:
            # 왼손: 엄지 x < 3번 x
            fingers.append(1 if lm_list[4][0] < lm_list[3][0] else 0)

        # 다른 손가락들 (y축, 팁 < PIP = 펴짐)
        tips = [8, 12, 16, 20]  # 검지, 중지, 약지, 새끼
        pip = [6, 10, 14, 18]

        for tip, pip_joint in zip(tips, pip):
            fingers.append(1 if lm_list[tip][1] < lm_list[pip_joint][1] else 0)

        return fingers
    
    def detect_gesture(self):
        fingers = self.fingers_up()
        if not fingers or len(fingers) != 5:
            return None

        finger_count = sum(fingers)
        
        # 주먹 (모든 손가락 접힘)
        if finger_count == 0:
            return "FIST"
        
        # 손 펴기 (4개 이상 펴짐)
        elif finger_count >= 4:
            return "FIVE"
        
        # V (검지+중지만 펴짐, 또는 검지만 펴짐)
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            return "V"
        elif fingers[1] == 1 and sum(fingers[2:]) == 0:
            return "V"
        
        # 엄지업 (엄지만 펴짐, 또는 엄지+하나만)
        elif fingers[0] == 1 and sum(fingers[1:]) <= 3:  # ← 1 → 3으로 완화
            return "THUMBS_UP"
        
        else:
            return "UNKNOWN"
