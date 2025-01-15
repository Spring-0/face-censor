# Face Detection and Censoring System

A Python-based system for detecting faces in images and videos using YOLOv8, with the ability to censor detected faces. The system is designed to be modular and extensible.

Currently does not include a user interface, but will be implementing one very soon.

## Features

- Face detection using YOLOv8
- Support for both image and video processing
- Modular censoring system (currently supports blur)
- Trained on the WIDER FACE dataset via Roboflow

## Demo

Input Image/Video
![Input Image](input.jpg)

Output Image
![Output Image](output.jpg)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Spring-0/face-censor.git
cd face-censor
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Roboflow API key:
```
ROBOFLOW_API_KEY=your_api_key_here
```

## Training the Model

The project uses the WIDER FACE dataset from Roboflow for training. To train the model:

1. Update this line in `training/training.py` if required:
```python
device="0"  # Set to "0" to utilize GPU, otherwise set to "cpu" to utilize CPU
```

2. Run the training script:
```
cd training
python3 training.py
```

## Usage

```python
from models.yolo_detector import YOLOFaceDetector
from censoring.blur import BlurCensor
from processor import MediaProcessor

# Initialize components
detector = YOLOFaceDetector()
censor = BlurCensor()
processor = MediaProcessor(detector, censor)
```
### Processing Images
```python
# Process an image
processor.process_image("input.jpg", "output.jpg")
```

### Processing Videos

```python
# Process a video
processor.process_video("input.mp4", "output.mp4")
```

## Requirements

- Python 3.8+
- PyTorch
- OpenCV
- Ultralytics YOLOv8
- Roboflow

See `requirements.txt` for complete list.

## License

GPU General Public License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## TODO

- [ ] Add emoji face masking
- [ ] Add GUI interface

