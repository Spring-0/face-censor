from models.face_detector import YOLOFaceDetector
from masking.text import TextCensor
from processor import MediaProcessor

def main():
    detector = YOLOFaceDetector()
    text_censor = TextCensor(text="HELLO", background_color="white", text_color="black", scale_factor=0.2)

    processor = MediaProcessor(detector, text_censor)
    processor.process_image("input.jpg", "output_emoji.jpg")
    
if __name__ == "__main__":
    main()