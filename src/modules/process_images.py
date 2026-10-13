import os
import traceback
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import torch
import yaml
from PIL import Image
from tqdm import tqdm
from transformers import AutoModelForImageTextToText, AutoProcessor
from db.document_processor import Document
from core.extract_metadata import extract_typed_metadata
from core.utilities import my_cprint, set_cuda_paths, quiet_transformers_loading_bars
from core.constants import VISION_MODELS, PROJECT_ROOT

set_cuda_paths()
quiet_transformers_loading_bars()

warnings.filterwarnings("ignore", message=".*Torch was not compiled with flash attention.*")

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff']

current_directory = PROJECT_ROOT
CACHE_DIR = current_directory / "models" / "vision"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_PROMPT_TEMPLATE = (
    "Describe this image in detail but do not repeat yourself. "
    "Your response should be a single paragraph of approximately {n} words, "
    "and aim for a consistent length regardless of how simple or complex the image is."
)

IMAGE_PROMPT_DEFAULT_WORDS = 125

VISION_MODEL_WORD_TARGETS = {
    'Liquid-VL - 480M':    130,
    'Liquid-VL - 1.6B':    120,
}

IMAGE_PROMPT = IMAGE_PROMPT_TEMPLATE.format(n=IMAGE_PROMPT_DEFAULT_WORDS)


def get_image_prompt(chosen_model: str) -> str:
    n = VISION_MODEL_WORD_TARGETS.get(chosen_model, IMAGE_PROMPT_DEFAULT_WORDS)
    return IMAGE_PROMPT_TEMPLATE.format(n=n)

def get_best_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'

def to_rgb(image):
    if image.mode in ("I;16", "I;16B", "I;16L", "I;16N", "I", "F"):
        arr = np.asarray(image, dtype=np.float64)
        peak = arr.max() if arr.size else 0.0
        if peak > 255:
            arr = arr * (255.0 / peak)
        elif image.mode == "F" and peak <= 1.0:
            arr = arr * 255.0
        image = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "L")
    if image.mode in ("RGBA", "LA", "PA", "RGBa", "La") or "transparency" in image.info:
        image = image.convert("RGBA")
        image = Image.alpha_composite(Image.new("RGBA", image.size, (255, 255, 255, 255)), image)
    return image if image.mode == "RGB" else image.convert("RGB")

def check_for_images(image_dir: Path) -> bool:
    try:
        filenames = os.listdir(str(image_dir))
        return any(Path(f).suffix.lower() in ALLOWED_EXTENSIONS for f in filenames)
    except FileNotFoundError:
        return False
    except OSError:
        return False

def run_loader_in_process(loader_func):
    try:
        return loader_func()
    except Exception as e:
        error_message = f"Error processing images: {e}\n\nTraceback:\n{traceback.format_exc()}"
        my_cprint(error_message, "red")
        return []


def choose_image_loader(model_config: dict | None = None, return_timing: bool = False):
    if model_config is None:
        cfg_path = Path('config.yaml')
        if not cfg_path.exists():
            raise FileNotFoundError("config.yaml not found and no model_config provided")
        with cfg_path.open('r', encoding='utf-8') as f:
            model_config = yaml.safe_load(f) or {}

    vision_cfg = (model_config.get('vision') or {})
    chosen_model = vision_cfg.get('chosen_model')
    if not chosen_model:
        raise ValueError("vision.chosen_model missing in config/model_config")

    if chosen_model not in VISION_MODELS:
        raise KeyError(f"Unknown vision model: {chosen_model}")
    loader_name = VISION_MODELS[chosen_model]['loader']

    loader_class = globals()[loader_name]
    loader = loader_class(model_config)

    image_dir = Path(os.environ.get("VECTORDB_SOURCE_DIR") or PROJECT_ROOT / "Docs_for_DB")
    if not check_for_images(image_dir):
        return ([], 0.0) if return_timing else []

    with ProcessPoolExecutor(1, initializer=set_cuda_paths) as executor:
        future = executor.submit(run_loader_in_process, loader.process_images)
        try:
            result = future.result()
        except Exception as e:
            my_cprint(f"Error occurred during image processing: {e}", "red")
            return ([], 0.0) if return_timing else []

        if isinstance(result, tuple) and len(result) == 2:
            processed_docs, processing_time = result
        else:
            processed_docs, processing_time = (result or []), 0.0

        processed_docs = processed_docs or []
        return (processed_docs, processing_time) if return_timing else processed_docs


class BaseLoader:
    def __init__(self, config):
        self.config = config
        self.device = get_best_device()
        self.model = None
        self.tokenizer = None
        self.processor = None

    @staticmethod
    def detect_dtype():
        if not torch.cuda.is_available():
            return torch.float32, "float32"
        use_bf16 = torch.cuda.get_device_capability()[0] >= 8
        return (torch.bfloat16, "bfloat16") if use_bf16 else (torch.float16, "float16")

    @staticmethod
    def normalize_response(text):
        return ' '.join(line.strip() for line in text.split('\n') if line.strip())

    def initialize_model_and_tokenizer(self):
        raise NotImplementedError

    def process_images(self):
        image_dir = Path(os.environ.get("VECTORDB_SOURCE_DIR") or PROJECT_ROOT / "Docs_for_DB")
        documents = []

        try:
            image_files = [file for file in image_dir.iterdir() if file.suffix.lower() in ALLOWED_EXTENSIONS]
        except OSError:
            image_files = []
            print(f"Error accessing directory {image_dir}")

        self.model, self.tokenizer, self.processor = self.initialize_model_and_tokenizer()
        print("Processing images.")
        start_time = time.time()
        with tqdm(total=len(image_files), unit="image") as progress_bar:
            for full_path in image_files:
                try:
                    with Image.open(full_path) as raw_image:
                        extracted_text = self.process_single_image(raw_image)
                        extracted_metadata = extract_typed_metadata(full_path, "image")
                        documents.append(Document(page_content=extracted_text, metadata=extracted_metadata))
                        progress_bar.update(1)
                except Exception as e:
                    print(f"{full_path.name}: Error processing image - {e}")
        total_time = time.time() - start_time
        print(f"Loaded {len(documents)} image(s).")
        print(f"Total image processing time: {total_time:.2f} seconds")
        my_cprint("Vision model removed from memory.", "red")
        return documents, total_time

    def process_single_image(self, raw_image):
        raise NotImplementedError


class loader_liquidvl(BaseLoader):
    def initialize_model_and_tokenizer(self):
        chosen_model = self.config['vision']['chosen_model']
        info = VISION_MODELS[chosen_model]
        source = info.get('model_path') or info['repo_id']
        cache_dir = CACHE_DIR / info.get('cache_dir', '')
        cache_dir.mkdir(parents=True, exist_ok=True)

        if torch.cuda.is_available():
            dtype, precision_str = self.detect_dtype()
            device_map = "auto"
        else:
            dtype = torch.float32
            precision_str = "float32"
            device_map = {"": "cpu"}

        model = AutoModelForImageTextToText.from_pretrained(
            source,
            dtype=dtype,
            cache_dir=cache_dir,
            device_map=device_map,
        ).eval()

        processor = AutoProcessor.from_pretrained(
            source,
            cache_dir=cache_dir,
        )

        if hasattr(processor, "tokenizer") and hasattr(processor.tokenizer, "add_bos_token"):
            processor.tokenizer.add_bos_token = False

        if torch.cuda.is_available():
            device_str = "CUDA"
        else:
            device_str = "CPU"
        my_cprint(f"{chosen_model} loaded into memory on {device_str} ({precision_str})", "green")

        return model, None, processor

    @torch.inference_mode()
    def process_single_image(self, raw_image):
        raw_image = to_rgb(raw_image)

        system_text = "You are a helpful multimodal assistant."

        chatml = (
            "<|startoftext|><|im_start|>system\n"
            f"{system_text}<|im_end|>\n"
            "<|im_start|>user\n"
            f"<image>{get_image_prompt(self.config['vision']['chosen_model'])}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )

        inputs = self.processor(
            text=[chatml],
            images=[[raw_image]],
            return_tensors="pt",
            use_image_special_tokens=True,
            do_image_splitting=True,
            min_image_tokens=64,
            max_image_tokens=256,
        )

        move_to = getattr(self.model, "device", None)
        if move_to is not None:
            inputs = inputs.to(move_to)

        input_len = inputs["input_ids"].shape[1]
        eos_id = self.processor.tokenizer.convert_tokens_to_ids("<|im_end|>")
        pad_id = self.processor.tokenizer.pad_token_id or eos_id

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,
            eos_token_id=eos_id,
            pad_token_id=pad_id,
        )

        new_tokens = outputs[:, input_len:]
        text = self.processor.batch_decode(new_tokens, skip_special_tokens=True)[0].strip()
        return self.normalize_response(text)
