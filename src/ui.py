from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import tempfile
import gradio as gr

from models.face_detector import YOLOFaceDetector
from masking.text import TextCensor
from masking.emoji import EmojiCensor
from masking.blur import BlurCensor
from processors.processor import MediaProcessor

@dataclass
class CensorSettings:
    type: Optional[str] = None
    # Blur settings
    blur_factor: Optional[int] = None
    # Emoji settings
    emoji: Optional[str] = None
    emoji_scale: Optional[float] = None
    # Text settings
    text: Optional[str] = None
    text_scale: Optional[float] = None
    draw_background: Optional[bool] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    font: Optional[str] = None


class FaceCensorUI:
    CENSOR_TYPES = ["Blur", "Text", "Emoji"]
    FONTS = ["arial.ttf", "times.ttf"]
    DEFAULT_SETTINGS = {
        "blur_factor": 99,
        "emoji": "😁",
        "emoji_scale": 1.0,
        "text": "Hello",
        "text_scale": 0.2,
        "draw_background": True,
        "background_color": "#000000",
        "text_color": "#00FF00",
        "font": "arial.ttf"
    }

    def __init__(self):
        self.detector = YOLOFaceDetector()

    def create_censor(self, settings):
        # Map censor name to censor object
        censor_map = {
            "Blur": lambda: BlurCensor(blur_factor=settings.blur_factor),
            "Emoji": lambda: EmojiCensor(
                emoji=settings.emoji,
                scale_factor=settings.emoji_scale,
                font="seguiemj.ttf"
            ),
            "Text": lambda: TextCensor(
                text=settings.text,
                scale_factor=settings.text_scale,
                draw_background=settings.draw_background,
                background_color=settings.background_color,
                text_color=settings.text_color,
                font=settings.font or "arial.ttf"
            )
        }
        
        if settings.type not in censor_map:
            raise ValueError(f"Unknown censor type: {settings.type}")
        
        return censor_map[settings.type]()

    def process_file(self, input_media, settings_dict):
        try:
            settings = CensorSettings(**settings_dict)
            censor = self.create_censor(settings)
            processor = MediaProcessor(self.detector, censor)
            
            temp_dir = Path(tempfile.mkdtemp())
            input_path = Path(input_media.name)
            
            if input_path.suffix.lower() in ('.mp4', '.avi', '.mov'):
                output_path = temp_dir / "output.mp4"
                processor.process_video(str(input_path), str(output_path))
            else:
                output_path = temp_dir / "output.jpg"
                processor.process_image(str(input_path), str(output_path))
                
            return str(output_path)
            
        except Exception as e:
            return f"Error processing media: {str(e)}"

    def create_ui(self):
        with gr.Blocks(title="Face Censor") as ui:
            gr.Markdown("# Censor Faces Automatically!")
            
            with gr.Tab("File Processing"):
                self._create_media_section()
                self._create_settings_section()
        
            with gr.Row():
                gr.Markdown(
                    """
                    ## [View source code on GitHub](https://github.com/Spring-0/face-censor)
                    *⭐ the repo to show support*
                    """
                )
                
            return ui

    def _create_media_section(self):
        with gr.Row():
            self.input_media = gr.File(label="Upload Image/Video")
            self.output_media = gr.File(label="Processed Output")

    def _create_settings_section(self):
        self.censor_type = gr.Dropdown(
            choices=self.CENSOR_TYPES,
            value=self.CENSOR_TYPES[0],
            label="Censoring Method"
        )

        self.blur_settings = self._create_blur_settings()
        self.emoji_settings = self._create_emoji_settings()
        self.text_settings = self._create_text_settings()
        
        self.process_btn = gr.Button("Process")
        
        self.censor_type.change(
            self._update_settings_visibility,
            inputs=[self.censor_type],
            outputs=[self.blur_settings, self.emoji_settings, self.text_settings]
        )
        
        self.process_btn.click(
            self._handle_processing,
            inputs=self._get_all_inputs(),
            outputs=[self.output_media]
        )

    def _create_blur_settings(self):
        with gr.Row(visible=True) as section:
            self.blur_factor = gr.Slider(
                minimum=1,
                maximum=199,
                value=self.DEFAULT_SETTINGS["blur_factor"],
                step=2,
                label="Blur Factor"
            )
            
        return section

    def _create_emoji_settings(self):
        with gr.Row(visible=False) as section:
            self.emoji = gr.Textbox(
                value=self.DEFAULT_SETTINGS["emoji"],
                label="Emoji"
            )
            
            self.emoji_scale = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=self.DEFAULT_SETTINGS["emoji_scale"],
                step=0.1,
                label="Emoji Scale Factor"
            )
            
        return section

    def _create_text_settings(self):
        with gr.Column(visible=False) as section:
            with gr.Row(equal_height=True):
                self.text = gr.Textbox(
                    value=self.DEFAULT_SETTINGS["text"],
                    label="Text"
                )
                
                self.text_scale = gr.Slider(
                    minimum=0.1,
                    maximum=2.0,
                    value=self.DEFAULT_SETTINGS["text_scale"],
                    step=0.1,
                    label="Text Scale Factor"
                )
                
            with gr.Row(equal_height=True):
                self.draw_background = gr.Checkbox(
                    value=self.DEFAULT_SETTINGS["draw_background"],
                    label="Draw Background",
                )
                
                self.background_color = gr.ColorPicker(
                    value=self.DEFAULT_SETTINGS["background_color"],
                    label="Background Color"
                )
                
            with gr.Row(equal_height=True):
                self.text_color = gr.ColorPicker(
                    value=self.DEFAULT_SETTINGS["text_color"],
                    label="Text Color"
                )
                
                self.font = gr.Dropdown(
                    choices=self.FONTS,
                    value=self.DEFAULT_SETTINGS["font"],
                    label="Font"
                )
                
        return section

    def _update_settings_visibility(self, censor_choice):
        return [
            gr.Row(visible=censor_choice=="Blur"),
            gr.Row(visible=censor_choice=="Emoji"),
            gr.Row(visible=censor_choice=="Text")
        ]

    def _get_all_inputs(self):
        return [
            self.input_media,
            self.censor_type,
            self.blur_factor,
            self.emoji,
            self.emoji_scale,
            self.text,
            self.text_scale,
            self.draw_background,
            self.background_color,
            self.text_color,
            self.font
        ]

    def _handle_processing(self, *args):
        input_media = args[0]
        settings_dict = {
            "type": args[1],
            "blur_factor": args[2],
            "emoji": args[3],
            "emoji_scale": args[4],
            "text": args[5],
            "text_scale": args[6],
            "draw_background": args[7],
            "background_color": args[8],
            "text_color": args[9],
            "font": args[10]
        }
        
        return self.process_file(input_media, settings_dict)
