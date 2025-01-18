import cv2
from .base import CensoringMethod
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class EmojiCensor(CensoringMethod):
    def __init__(self, emoji, font_path="seguiemj.ttf", scale_factor=1.0):
        self.emoji = emoji
        self.font_path = font_path
        self.scale_factor = scale_factor

    def apply(self, frame, bbox):
        x1, y1, x2, y2 = bbox[:4]

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        font_size = int(max(x2-x1, y2-y1) * self.scale_factor)

        try:
            font_app = ImageFont.truetype(self.font_path, font_size)
        except OSError as e:
            raise ValueError(f"Cannot open resource at {self.font_path}")

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(rgb_frame)

        draw = ImageDraw.Draw(pil_frame)
        draw.text(xy=(center_x, center_y), text=self.emoji, anchor="mm", font=font_app, embedded_color=True)

        out_image = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        return out_image
