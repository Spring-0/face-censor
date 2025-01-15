import cv2
from .base import CensoringMethod

class BlurCensor(CensoringMethod):
    def __init__(self, blur_factor=99):
        self.blur_factor = blur_factor
        
    def apply(self, frame, bbox):
        x1, y1, x2, y2 = bbox[:4]
        roi = frame[y1:y2, x1:x2]
        
        blurred = cv2.GaussianBlur(roi, (self.blur_factor, self.blur_factor), 0)
        frame[y1:y2, x1:x2] = blurred
        return frame
        