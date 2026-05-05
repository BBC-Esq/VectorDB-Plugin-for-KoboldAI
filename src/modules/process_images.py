import os
import traceback
import inspect
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import torch
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
import yaml
from PIL import Image
from tqdm import tqdm
from transformers import (
    AutoModel,
    AutoTokenizer,
    AutoProcessor,
    BitsAndBytesConfig,
    AutoModelForImageTextToText,
)
from db.document_processor import Document
from core.extract_metadata import extract_typed_metadata
from core.utilities import my_cprint, has_bfloat16_support, set_cuda_paths
from core.constants import VISION_MODELS, PROJECT_ROOT

set_cuda_paths()

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
    'Liquid-VL - 3B':      120,
    'InternVL3 - 1b':      145,
    'InternVL3 - 2b':      155,
    'InternVL3 - 8b':      120,
    'InternVL3 - 14b':     125,
    'Qwen VL - 3b':        125,
}

IMAGE_PROMPT = IMAGE_PROMPT_TEMPLATE.format(n=IMAGE_PROMPT_DEFAULT_WORDS)

def get_image_prompt(chosen_model: str) -> str:
    n = VISION_MODEL_WORD_TARGETS.get(chosen_model, IMAGE_PROMPT_DEFAULT_WORDS)
    return IMAGE_PROMPT_TEMPLATE.format(n=n)

def get_best_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'

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

    image_dir = PROJECT_ROOT / "Docs_for_DB"
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
        use_bf16 = torch.cuda.get_device_capability()[0] >= 8
        return (torch.bfloat16, "bfloat16") if use_bf16 else (torch.float16, "float16")

    @staticmethod
    def normalize_response(text):
        return ' '.join(line.strip() for line in text.split('\n') if line.strip())

    def initialize_model_and_tokenizer(self):
        raise NotImplementedError

    def process_images(self):
        image_dir = PROJECT_ROOT / "Docs_for_DB"
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


class loader_internvl(BaseLoader):
    def initialize_model_and_tokenizer(self):
        chosen_model = self.config['vision']['chosen_model']
        info = VISION_MODELS[chosen_model]
        cache_dir = CACHE_DIR / info["cache_dir"]
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        if self.device == "cuda":
            dtype, precision_str = self.detect_dtype()

            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=dtype,
                bnb_4bit_quant_type="nf4",
                llm_int8_skip_modules=[
                    "vision_model",
                    "language_model.model.norm", 
                    "language_model.output",
                    "language_model.model.rotary_emb",
                    "language_model.lm_head",
                    "mlp1"
                ]
            )
            model = AutoModel.from_pretrained(
                info['repo_id'],
                quantization_config=quant_config,
                torch_dtype=dtype,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                cache_dir=cache_dir,
                token=False
            ).eval()
            device_str = "CUDA"
        else:
            dtype = torch.float32
            precision_str = "float32"
            model = AutoModel.from_pretrained(
                info['repo_id'],
                torch_dtype=dtype,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                cache_dir=cache_dir,
                token=False,
                device_map={"": "cpu"}
            ).eval()
            device_str = "CPU"

        self.model_dtype = dtype
        my_cprint(f"{chosen_model} loaded into memory on {device_str} ({precision_str})", "green")

        tokenizer = AutoTokenizer.from_pretrained(
            info['repo_id'],
            trust_remote_code=True,
            cache_dir=cache_dir,
            token=False
        )

        return model, tokenizer, None

    def find_closest_aspect_ratio(self, aspect_ratio, ratios, w, h, sz):
        best_diff = float('inf')
        best = (1, 1)
        area = w * h
        for r in ratios:
            ar = r[0] / r[1]
            diff = abs(aspect_ratio - ar)
            if diff < best_diff or (diff == best_diff and area > 0.5 * sz * sz * r[0] * r[1]):
                best_diff = diff
                best = r

        return best

    def _build_transform(self, size):
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        return T.Compose([
            T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
            T.Resize((size, size), interpolation=InterpolationMode.LANCZOS, antialias=True),
            T.ToTensor(),
            T.Normalize(mean=mean, std=std)
        ])

    def dynamic_preprocess(self, img, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
        w, h = img.size
        ar = w / h
        ratios = sorted(
            {(i, j)
             for n in range(min_num, max_num + 1)
             for i in range(1, n + 1)
             for j in range(1, n + 1)
             if i * j <= max_num and i * j >= min_num},
            key=lambda x: x[0] * x[1]
        )
        best = self.find_closest_aspect_ratio(ar, ratios, w, h, image_size)
        tw, th = image_size * best[0], image_size * best[1]
        resized = img.resize((tw, th))
        blocks = best[0] * best[1]
        cols = tw // image_size
        parts = []
        for i in range(blocks):
            x = (i % cols) * image_size
            y = (i // cols) * image_size
            parts.append(resized.crop((x, y, x + image_size, y + image_size)))
        if use_thumbnail and len(parts) != 1:
            parts.append(img.resize((image_size, image_size)))

        return parts

    def _prepare_image(self, raw_image, input_size=448, max_num=24):
        imgs = self.dynamic_preprocess(raw_image, image_size=input_size, use_thumbnail=True, max_num=max_num)
        tf = self._build_transform(input_size)

        return torch.stack([tf(im) for im in imgs])

    @torch.inference_mode()
    def process_single_image(self, raw_image):
        pv = self._prepare_image(raw_image).to(self.model_dtype).to(self.device)

        question = f"<image>\n{get_image_prompt(self.config['vision']['chosen_model'])}"

        gen_cfg = {
            'num_beams': 1,
            'max_new_tokens': 512,
            'do_sample': False,
            'pad_token_id': self.tokenizer.pad_token_id
        }
        resp = self.model.chat(self.tokenizer, pv, question, gen_cfg)

        return self.normalize_response(resp)


class loader_qwenvl(BaseLoader):
    def initialize_model_and_tokenizer(self):
        chosen_model = self.config['vision']['chosen_model']
        model_info = VISION_MODELS[chosen_model]
        model_id = model_info['repo_id']
        save_dir = model_info['cache_dir']
        cache_dir = CACHE_DIR / save_dir
        cache_dir.mkdir(parents=True, exist_ok=True)

        dtype, _ = self.detect_dtype()

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=dtype,
            bnb_4bit_use_double_quant=True,
            llm_int8_threshold=6.0,
            llm_int8_skip_modules=[
                "lm_head",
                "merger",
                "visual.blocks.0.attn",
                "visual.blocks.0.mlp",
                "visual.blocks.1.attn",
                "visual.blocks.1.mlp",
                "visual.blocks.2.attn",
                "visual.blocks.2.mlp",
                "visual.blocks.3.attn",
                "visual.blocks.3.mlp",
                "visual.blocks.4.attn",
                "visual.blocks.5.mlp",
                "visual.blocks.7.attn",
                "visual.blocks.7.mlp",
                "visual.blocks.8.mlp",
                "visual.blocks.10.mlp",
                "visual.blocks.12.mlp",
                "visual.blocks.13.mlp",
                "visual.blocks.14.attn",
                "visual.blocks.14.mlp",
                "visual.blocks.15.attn",
                "visual.blocks.15.mlp",
                "visual.blocks.17.mlp",
                "visual.blocks.31.mlp.down_proj"
            ]
        )

        processor = AutoProcessor.from_pretrained(
            model_id,
            backend="torchvision",
            min_pixels=28*28,
            max_pixels=1280*28*28,
            trust_remote_code=True,
            cache_dir=cache_dir,
            token=False
        )

        model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            cache_dir=cache_dir,
            token=False,
            device_map="auto",
        )
        model.eval()

        _, precision_str = self.detect_dtype()
        device_str = "CUDA" if self.device == "cuda" else "CPU"
        my_cprint(f"{chosen_model} loaded into memory on {device_str} ({precision_str})", "green")

        return model, None, processor

    @torch.inference_mode()
    def process_single_image(self, raw_image):

        prompt = (
            "<|im_start|>user\n"
            f"{get_image_prompt(self.config['vision']['chosen_model'])} <|vis_start|><|image_pad|><|vis_end|>\n"
            "<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        inputs = self.processor(
            images=raw_image,
            text=prompt,
            return_tensors="pt"
        ).to(self.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            top_k=None,
            top_p=None,
            num_beams=1,
            temperature=None
        )
        response = self.processor.decode(output[0], skip_special_tokens=True)
        response = response.split('assistant')[-1].strip()

        return self.normalize_response(response)


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
            trust_remote_code=True,
            torch_dtype=dtype,
            cache_dir=cache_dir,
            device_map=device_map,
        ).eval()

        processor = AutoProcessor.from_pretrained(
            source,
            trust_remote_code=True,
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
        if raw_image.mode != "RGB":
            raw_image = raw_image.convert("RGB")

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
        text = self.processor.decode(new_tokens[0], skip_special_tokens=True).strip()
        return self.normalize_response(text)
