import mediapipe as mp
import cv2

class Detector:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
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
    
    def fingers_up(self):
        """
        Returns a list of 5 elements (1 for up, 0 for down)
        Thumb, Index, Middle, Ring, Pinky
        """
        lm_list = self.get_landmarks()
        if not lm_list:
            return []

        fingers = []

        # Thumb
        if lm_list[4][0] > lm_list[3][0]:  # simple check, works for right hand
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers (Index, Middle, Ring, Pinky)
        tips = [8, 12, 16, 20]
        pip = [6, 10, 14, 18]

        for tip, pip_joint in zip(tips, pip):
            if lm_list[tip][1] < lm_list[pip_joint][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def detect_gesture(self):
        fingers = self.fingers_up()
        if not fingers:
            return None

        # Map finger states to gesture
        if fingers == [0,0,0,0,0]:
            return "FIST"
        elif fingers == [1,1,1,1,1]:
            return "FIVE"
        elif fingers == [0,1,1,0,0]:
            return "V"
        elif fingers == [1,0,0,0,0]:
            return "THUMBS_UP"
        else:
            return "UNKNOWN"

