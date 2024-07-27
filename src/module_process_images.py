import datetime
import gc
import os
import logging
import traceback
import platform
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import torch
import yaml
from PIL import Image
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM, AutoModel, AutoTokenizer, AutoProcessor, BlipForConditionalGeneration, BlipProcessor,
    LlamaTokenizer, LlavaForConditionalGeneration, BitsAndBytesConfig
)

from langchain_community.docstore.document import Document

from extract_metadata import extract_image_metadata
from utilities import my_cprint
from constants import VISION_MODELS

datasets_logger = logging.getLogger('datasets')
datasets_logger.setLevel(logging.WARNING)

logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger().setLevel(logging.WARNING)

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff']

current_directory = Path(__file__).parent
VISION_DIR = current_directory / "models" / "vision"
VISION_DIR.mkdir(parents=True, exist_ok=True)

def get_best_device():
    if torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'

def check_for_images(image_dir):
    return any(
        os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS
        for file in os.listdir(image_dir)
    )

def run_loader_in_process(loader_func):
    try:
        return loader_func()
    except Exception as e:
        error_message = f"Error processing images: {e}\n\nTraceback:\n{traceback.format_exc()}"
        my_cprint(error_message, "red")
        return []

def choose_image_loader():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    chosen_model = config["vision"]["chosen_model"]

    if chosen_model == 'Moondream2':
        loader_func = loader_moondream(config).process_images
    elif chosen_model in ["Florence-2-large", "Florence-2-base"]:
        loader_func = loader_florence2(config).process_images
    else:
        my_cprint("No valid image model specified in config.yaml", "red")
        return []

    script_dir = os.path.dirname(__file__)
    image_dir = os.path.join(script_dir, "Docs_for_DB")

    if not check_for_images(image_dir):
        print("No images selected for processing...")
        return []

    with ProcessPoolExecutor(1) as executor:
        future = executor.submit(run_loader_in_process, loader_func)
        try:
            processed_docs = future.result()
        except Exception as e:
            my_cprint(f"Error occurred during image processing: {e}", "red")
            return []

        if processed_docs is None:
            return []
        return processed_docs


class BaseLoader:
    def __init__(self, config):
        self.config = config
        self.device = get_best_device()
        self.model = None
        self.tokenizer = None
        self.processor = None

    def initialize_model_and_tokenizer(self):
        raise NotImplementedError("Subclasses must implement initialize_model_and_tokenizer method")

    def process_images(self):
        script_dir = os.path.dirname(__file__)
        image_dir = os.path.join(script_dir, "Docs_for_DB")
        documents = []
        allowed_extensions = ALLOWED_EXTENSIONS

        image_files = [file for file in os.listdir(image_dir) if os.path.splitext(file)[1].lower() in allowed_extensions]

        self.model, self.tokenizer, self.processor = self.initialize_model_and_tokenizer()

        print("Processing images...")
        
        total_start_time = time.time()

        with tqdm(total=len(image_files), unit="image") as progress_bar:
            for file_name in image_files:
                full_path = os.path.join(image_dir, file_name)
                try:
                    with Image.open(full_path) as raw_image:
                        extracted_text = self.process_single_image(raw_image)
                        extracted_metadata = extract_image_metadata(full_path)
                        document = Document(page_content=extracted_text, metadata=extracted_metadata)
                        documents.append(document)
                        progress_bar.update(1)
                except Exception as e:
                    print(f"{file_name}: Error processing image - {e}")

        total_end_time = time.time()
        total_time_taken = total_end_time - total_start_time
        print(f"Loaded {len(documents)} image(s)...")
        print(f"Total image processing time: {total_time_taken:.2f} seconds")

        my_cprint("Vision model removed from memory.", "red")

        return documents

    def process_single_image(self, raw_image):
        raise NotImplementedError("Subclasses must implement process_single_image method")


class loader_moondream(BaseLoader):
    def initialize_model_and_tokenizer(self):
        chosen_model = self.config['vision']['chosen_model']
        model_id = VISION_MODELS[chosen_model]['repo_id']
        cache_dir=VISION_DIR
        
        model = AutoModelForCausalLM.from_pretrained(model_id, 
                                                     trust_remote_code=True, 
                                                     revision="2024-07-23",
                                                     torch_dtype=torch.float16,
                                                     cache_dir=cache_dir,
                                                     low_cpu_mem_usage=True).to(self.device)

        my_cprint(f"Moondream2 vision model loaded into memory...", "green")
        
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision="2024-05-20", cache_dir=cache_dir)
        
        return model, tokenizer, None
    
    @torch.inference_mode()
    def process_single_image(self, raw_image):
        enc_image = self.model.encode_image(raw_image)
        summary = self.model.answer_question(enc_image, "Describe what this image depicts in as much detail as possible.", self.tokenizer)
        return summary


class loader_florence2(BaseLoader):
    def __init__(self, config):
        super().__init__(config)
        from utilities import my_cprint, get_device_and_precision
        self.my_cprint = my_cprint
        self.get_device_and_precision = get_device_and_precision
        warnings.filterwarnings("ignore", message=".*Torch was not compiled with flash attention.*")

    def initialize_model_and_tokenizer(self):
        chosen_model = self.config['vision']['chosen_model']
        model_id = VISION_MODELS[chosen_model]['repo_id']
        cache_dir=VISION_DIR
        
        model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, cache_dir=cache_dir)
        processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, cache_dir=cache_dir)

        device_type, precision_type = self.get_device_and_precision()
        
        if device_type == "cuda":
            self.device = torch.device("cuda")
            model = model.to(self.device)
        else:
            self.device = torch.device("cpu")
        
        if precision_type == "float16":
            model = model.half()
        elif precision_type == "bfloat16":
            model = model.bfloat16()
        
        self.my_cprint(f"{chosen_model} loaded with {precision_type}.", color="green")
        
        self.precision_type = precision_type
        return model, None, processor

    @torch.inference_mode()
    def process_single_image(self, raw_image):
        prompt = "<MORE_DETAILED_CAPTION>"
        inputs = self.processor(text=prompt, images=raw_image, return_tensors="pt")
        
        if self.device.type == "cuda":
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        if self.precision_type != "float32":
            inputs["pixel_values"] = inputs["pixel_values"].to(getattr(torch, self.precision_type))
        
        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=1,
            do_sample=False,
            early_stopping=False
        )
        
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed_answer = self.processor.post_process_generation(generated_text, task=prompt, image_size=(raw_image.width, raw_image.height))
        
        return parsed_answer['<MORE_DETAILED_CAPTION>']
