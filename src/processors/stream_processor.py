import cv2
from .processor import MediaProcessor
import subprocess

class LiveStreamProcessor:
    def __init__(self, detector, censor):
        self.detector = detector
        self.censor = censor
        self.processor = MediaProcessor(detector, censor)
        
    def process_stream(self,
                       source,
                       output_type=None,
                       output_dest=None,
                       conf_thresh=0.4,
                       preview_stream=False):

        capture = cv2.VideoCapture(source)
        if not capture.isOpened():
            raise ValueError(f"Could not open video source {source}")
            
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        
        output = self.initialize_output(output_type, output_dest, width, height, fps)
        
        try:
            while True:
                ret, frame = capture.read()
                if not ret:
                    break
                
                detections = self.detector.detect(frame)
                for bbox in detections:
                    if bbox[4] >= conf_thresh:
                        frame = self.censor.apply(frame, bbox)
                
                if output_type == "rtmp":
                    output.stdin.write(frame.tobytes())
                else:
                    raise ValueError(f"Invalid output_type: {output_type}, try 'rtmp'?")
                
                if preview_stream:
                    cv2.imshow("Stream Preview", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    
        finally:
            capture.release()
            if output:
                self.cleanup_output(output, output_type)
            cv2.destroyAllWindows()
    
    def initialize_output(self, output_type, output_dest, width, height, fps):
        if output_dest == None: 
            raise ValueError("output_dest cannot be None, provide valid output destination.")
        
        if output_type == "rtmp":
            command = [
                "ffmpeg",
                "-y",  # Overwrite output files
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}",
                "-r", str(fps),
                "-i", "-",  # Input from pipe
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                "-f", "flv",
                output_dest  # RTMP URL
            ]
            return subprocess.Popen(command, stdin=subprocess.PIPE)    
        return None
    
    def cleanup_output(self, output, output_type):
        if output_type == "rtmp":
            output.stdin.close()
            output.wait()
