import cv2
from .text import TextCensor
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class EmojiCensor(TextCensor):
    def __init__(self, emoji, font_path="seguiemj.ttf", scale_factor=1.0):
        super().__init__(
            text=emoji,
            font_path=font_path,
            scale_factor=scale_factor,
            text_color=None,
            draw_background=False
        )

    def draw_overlay(self, draw, x, y, font):
        draw.text(
            xy=(x, y),
            text=self.text,
            anchor="mm",
            font=font,
            embedded_color=True
        )


