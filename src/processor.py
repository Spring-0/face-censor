import cv2

class MediaProcessor:
    def __init__(self, detector, censor):
        self.detector = detector
        self.censor = censor
        
    def process_image(self, image_path, output_path, conf_thresh = 0.6):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")
        
        detections = self.detector.detect(image)
        
        for bbox in detections:
            if bbox[4] >= conf_thresh:
                image = self.censor.apply(image, bbox)
                
        cv2.imwrite(output_path, image)
        return output_path
    
    def process_video(self, video_path, output_path, conf_thresh = 0.6):
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise ValueError(f"Could not open video at {video_path}")
        
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        try:
            while capture.isOpened():
                ret, frame = capture.read()
                if not ret: break
                
                detections = self.detector.detect(frame)
                
                for bbox in detections:
                    if bbox[4] >= conf_thresh:
                        frame = self.censor.apply(frame, bbox)
                        
                out.write(frame)
        finally:
            capture.release()
            out.release()
            
        return output_path