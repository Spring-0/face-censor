from .base import CensoringMethod
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

class TextCensor(CensoringMethod):
    def __init__(self,
                 text,
                 font_path="arial.ttf",
                 scale_factor=0.5,
                 text_color="white",
                 background_color=None,
                 draw_background=True):
        
        self.text = text
        self.font_path = font_path
        self.scale_factor = scale_factor
        self.text_color = text_color
        self.background_color = background_color
        self.draw_background = draw_background

    def apply(self, frame, bbox):
        x1, y1, x2, y2 = bbox[:4]
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        font_size = int(max(x2-x1, y2-y1) * self.scale_factor)

        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except OSError as e:
            raise ValueError(f"Could not open file at {self.font_path}")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(rgb_frame)
        draw = ImageDraw.Draw(pil_frame)

        if self.draw_background and self.background_color:
            draw.rectangle([x1, y1, x2, y2], fill=self.background_color)

        self.draw_overlay(draw, center_x, center_y, font)

        out_image = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        return out_image
    
    def draw_overlay(self, draw, x, y, font):
        draw.text(
            xy=(x, y),
            text=self.text,
            anchor="mm",
            font=font,
            fill=self.text_color
        )