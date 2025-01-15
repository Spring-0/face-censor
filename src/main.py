from models.face_detector import YOLOFaceDetector
from masking.blur import BlurCensor
from processor import MediaProcessor

def main():
    detector = YOLOFaceDetector()
    censor = BlurCensor()
    processor = MediaProcessor(detector, censor)
    
    processor.process_image("input.jpg", "output.jpg")
    processor.process_video("input.mp4", "output.mp4")
    
if __name__ == "__main__":
    main()