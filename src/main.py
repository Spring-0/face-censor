""" EXAMPLE CODE """ 
# from models.face_detector import YOLOFaceDetector
# from masking.text import TextCensor
# from masking.emoji import EmojiCensor
# from masking.blur import BlurCensor

# from processors.stream_processor import LiveStreamProcessor
# from processors.processor import MediaProcessor

# def main():
    # load_dotenv()
    
    #Initialize detector
    # detector = YOLOFaceDetector()
    
    # Using Text Masking
    # text_censor = TextCensor(text="HELLO", # The text to draw on faces
    #     draw_background=True, # Control whether to draw solid background behind text
    #     background_color="black", # The color of the solid background
    #     text_color="green", # The color of the text
    #     font="arial.ttf", # The path to font to use, defaults to 'arial.ttf'
    #     scale_factor=0.2 # The text size scaling factor
    # )
    
    # Using Emoji Masking
    # emoji_censor = EmojiCensor(
    #     emoji="😁", # The emoji you want to use to mask faces
    #     font="seguiemj.ttf", # The path to the emoji font file, by default uses "seguiemj.ttf"
    #     scale_factor=1.0 # The emoji size scaling factor in percentage
    # )
    
    # Using blur masking
    # blur_censor = BlurCensor(
    #     blur_factor=71 # The strength of the blur effect, defaults to 99
    # )
    
    # Create batch media processor, specifying masking method and detector.
    # processor = MediaProcessor(detector, blur_censor)
    
    # Process image
    # processor.process_image("assets/input.jpg", "assets/output_blur.jpg")
    
    # Process video
    # processor.process_video("assets/input.mp4", "assets/output.mp4")
    
    # Create live stream processor, specifying masking method and detector.
    #live_processor = LiveStreamProcessor(detector, blur_censor)
    
    # Process RTMP stream.
    #live_processor.process_stream(
    #    source="rtmp://localhost/live/livestream", # I used https://github.com/ossrs/srs for testing
    #    output_type="rtmp",
    #    output_dest=f"rtmp://jfk.contribute.live-video.net/app/{os.getenv('STREAM_KEY')}" # Tested on twitch
    #)
    
from ui import FaceCensorUI
    
if __name__ == "__main__":
    ui = FaceCensorUI()
    interface = ui.create_ui()
    interface.launch(pwa=True, server_name="0.0.0.0")