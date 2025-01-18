from models.face_detector import YOLOFaceDetector
from masking.blur import BlurCensor
from masking.emoji import EmojiCensor
from processor import MediaProcessor

def main():
    detector = YOLOFaceDetector()
    emoji_sensor = EmojiCensor("😁")
    processor = MediaProcessor(detector, emoji_sensor)
    
    processor.process_image("input.jpg", "output_emoji.jpg")
    
if __name__ == "__main__":
    main()