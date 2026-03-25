# Open the webcam
# Read frames continuously
# Return the frame to the main program

import cv2

class Camera:
    def __init__(self, camera_index=0, width= 640, height=480):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        '''Returns the current frame from the webcam.'''
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        '''Releases the camera when done.'''
        self.cap.release()
        cv2.destroyAllWindows()
