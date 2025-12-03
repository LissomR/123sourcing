from django.apps import AppConfig
from paddleocr import PaddleOCR
from transformers import pipeline, AutoTokenizer, AutoModelForDocumentQuestionAnswering, AutoProcessor, AutoModelForZeroShotImageClassification
from paddlenlp import Taskflow
import torch
from custom_lib.logger import BaseLog
from ultralytics import YOLO
from api_channel.settings import MODELS_PATH
logger = BaseLog()


class DocQueryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_extraction'

    def ready(self):
        try:
            global stamp_detection_model, document_classifier_model, ocr_inference, cpu_model_pipe, gpu_model_pipe, metaClip_preprocess, metaClip_inference
            device = "cpu"  # Force CPU mode for local development
            
            # Initialize None for models not loaded in CPU mode
            gpu_model_pipe = None
            metaClip_preprocess = None
            metaClip_inference = None

            cpu_model_directory = f"{MODELS_PATH}/cpu-model/model"
            cpu_model_tokenizer_directory = f"{MODELS_PATH}/cpu-model/tokenizers"
            clip_directory = f"{MODELS_PATH}/metaClip/model"

            # Load OCR model
            ocr_inference = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
            logger.print("✅ OCR model loaded successfully (CPU mode).")

            # Load CPU model for document QA
            cpu_tokenizer = AutoTokenizer.from_pretrained(cpu_model_tokenizer_directory)
            cpu_model = AutoModelForDocumentQuestionAnswering.from_pretrained(cpu_model_directory)
            cpu_model.to(device) 
            cpu_model_pipe = pipeline("document-question-answering", model=cpu_model, tokenizer=cpu_tokenizer, device=-1)
            logger.print("✅ LayoutLM CPU model loaded successfully.")

            # GPU model - DISABLED for CPU mode
            # gpu_model_pipe = Taskflow("document_intelligence", lang="en", task_path= f"{MODELS_PATH}/gpu-model/model")
            logger.print("⚠️  GPU model disabled (CPU mode active).")

            # MetaCLIP - Load if available, otherwise skip
            try:
                metaClip_preprocess = AutoProcessor.from_pretrained("facebook/metaclip-b16-fullcc2.5b")
                metaClip_inference = AutoModelForZeroShotImageClassification.from_pretrained(clip_directory, torch_dtype=torch.float32).to(device)
                logger.print("✅ Image similarity model loaded successfully.")
            except Exception as clip_error:
                logger.print(f"⚠️  MetaCLIP model not loaded: {str(clip_error)}")
                metaClip_preprocess = None
                metaClip_inference = None

            # Load YOLO models
            stamp_detection_model = YOLO(f'{MODELS_PATH}/yoloV8/stamp_detection_model.pt')
            document_classifier_model = YOLO(f'{MODELS_PATH}/yoloV8/document_classifier.pt')
            logger.print("✅ YOLO models loaded successfully.")


        except Exception as e:
            logger.print(f"❌ Error loading model: {str(e)}")
