from ultralytics import YOLO
from roboflow import Roboflow
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

class ModelTrainer:
    def __init__(self, roboflow_api_key):
        self.rf = Roboflow(api_key=roboflow_api_key)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def download_dataset(self, project_name, project_version, workspace):
        self.logger.info(f"Downloading dataset: {project_name} v{project_version}")
        project = self.rf.workspace(workspace).project(project_name)
        dataset = project.version(project_version).download("yolov8", "data\\raw")
        print(dataset.location)
        return dataset.location
    
    def train(
        self,
        data_yaml,
        model_type = "yolov8n.pt",
        epochs = 30,
        imgsz = 640,
        batch_size = 16,
        device = "0"
    ):
        self.logger.info("Starting training process")
        
        model = YOLO(model_type)
        
        results = model.train(
            data = data_yaml,
            epochs = epochs,
            imgsz = imgsz,
            batch = batch_size,
            device = device,
            project = "runs/train",
            name = "face_detection"
        )
        
        self.logger.info("Training Complete")
        return results
    
def main():          
    load_dotenv()     
    trainer = ModelTrainer(os.getenv("ROBOFLOW_API_KEY"))
    
    data_path = trainer.download_dataset(
        workspace="large-benchmark-datasets",
        project_name="wider-face-ndtcz",
        project_version=1
    )
    
    trainer.train(
        data_yaml=f"{data_path}\\data.yaml",
        epochs=20,
        batch_size=16,
        device="0"
    )
    
if __name__ == "__main__":
    main()