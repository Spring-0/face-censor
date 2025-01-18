from models.face_detector import YOLOFaceDetector
from masking.text import TextCensor
from masking.emoji import EmojiCensor
from masking.blur import BlurCensor

from processor import MediaProcessor

def main():
    #Initialize detector
    detector = YOLOFaceDetector()
    
    # Using Text Masking
    text_censor = TextCensor(text="HELLO", # The text to draw on faces
        draw_background=True, # Control whether to draw solid background behind text
        background_color="black", # The color of the solid background
        text_color="green", # The color of the text
        font="arial.ttf", # The path to font to use, defaults to 'arial.ttf'
        scale_factor=0.2 # The text size scaling factor
    )
    
    # Using Emoji Masking
    emoji_censor = EmojiCensor(
        emoji="😁", # The emoji you want to use to mask faces
        font="seguiemj.ttf", # The path to the emoji font file, by default uses "seguiemj.ttf"
        scale_factor=1.0 # The emoji size scaling factor in percentage
    )
    
    # Using blur masking
    blur_censor = BlurCensor(
        blur_factor=70 # The strength of the blur effect, defaults to 99 (which is max)
    )
    
    # Specify desired masking
    processor = MediaProcessor(detector, text_censor)
    
    # Process image
    processor.process_image("assets/input.jpg", "assets/output_text.jpg")
    
    # Process video
    processor.process_video("assets/input.mp4", "assets/output.mp4")
    
if __name__ == "__main__":
    main()