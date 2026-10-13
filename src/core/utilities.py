import os
import logging
import sys
from pathlib import Path
import re

import torch
import yaml
from termcolor import cprint

from core.cuda_paths import set_cuda_paths


def clean_triton_cache():
    import shutil
    from pathlib import Path

    triton_cache_dir = Path.home() / '.triton' / 'cache'

    if triton_cache_dir.exists():
        try:
            print(f"\nRemoving Triton cache at {triton_cache_dir}...")
            shutil.rmtree(triton_cache_dir)
            print("\033[92mTriton cache successfully removed.\033[0m")
            return True
        except Exception as e:
            print(f"\033[91mWarning: Failed to remove Triton cache: {e}\033[0m")
            return False
    else:
        print("\nNo Triton cache found to clean.")
        return True

def normalize_chat_text(text):
    def split_num(num):
        num = num.group()
        if '.' in num:
            return num
        elif ':' in num:
            h, m = [int(n) for n in num.split(':')]
            if m == 0:
                return f"{h} o'clock"
            elif m < 10:
                return f'{h} oh {m}'
            return f'{h} {m}'
        year = int(num[:4])
        if year < 1100 or year % 1000 < 10:
            return num
        left, right = num[:2], int(num[2:4])
        s = 's' if num.endswith('s') else ''
        if 100 <= year % 1000 <= 999:
            if right == 0:
                return f'{left} hundred{s}'
            elif right < 10:
                return f'{left} oh {right}{s}'
        return f'{left} {right}{s}'

    def flip_money(m):
        m = m.group()
        bill = 'dollar' if m[0] == '$' else 'pound'
        if m[-1].isalpha():
            return f'{m[1:]} {bill}s'
        elif '.' not in m:
            s = '' if m[1:] == '1' else 's'
            return f'{m[1:]} {bill}{s}'
        b, c = m[1:].split('.')
        s = '' if b == '1' else 's'
        c = int(c.ljust(2, '0'))
        coins = f"cent{'' if c == 1 else 's'}" if m[0] == '$' else ('penny' if c == 1 else 'pence')
        return f'{b} {bill}{s} and {c} {coins}'

    def point_num(num):
        a, b = num.group().split('.')
        return ' point '.join([a, ' '.join(b)])

    text = text.replace('§', ' section ')

    text = text.replace(chr(8216), "'").replace(chr(8217), "'")
    text = text.replace('«', '"').replace('»', '"')
    text = text.replace(chr(8220), '"').replace(chr(8221), '"')

    text = re.sub(r'\bD[Rr]\.(?= [A-Z])', 'Doctor', text)
    text = re.sub(r'\b(?:Mr\.|MR\.(?= [A-Z]))', 'Mister', text)
    text = re.sub(r'\b(?:Ms\.|MS\.(?= [A-Z]))', 'Miss', text)
    text = re.sub(r'\b(?:Mrs\.|MRS\.(?= [A-Z]))', 'Mrs', text)

    text = re.sub(r'\d*\.\d+|\b\d{4}s?\b|(?<!:)\b(?:[1-9]|1[0-2]):[0-5]\d\b(?!:)', split_num, text)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)
    text = re.sub(r'(?i)[$£]\d+(?:\.\d+)?(?: hundred| thousand| (?:[bm]|tr)illion)*\b|[$£]\d+\.\d\d?\b', flip_money, text)
    text = re.sub(r'\d*\.\d+', point_num, text)

    text = re.sub(r'[^\S \n]', ' ', text)
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'(?<=\n) +(?=\n)', '', text)

    text = text.strip()
    text = re.sub(r'^[^a-zA-Z]*', '', text)
    text = re.sub(r'\n+', ' ', text)

    return text.strip()


def get_model_native_precision(embedding_model_name, vector_models=None):
    if vector_models is None:
        from core.constants import VECTOR_MODELS
        vector_models = VECTOR_MODELS

    logging.debug(f"Looking for precision for model: {embedding_model_name}")
    model_name = os.path.basename(embedding_model_name)
    repo_style_name = model_name.replace('--', '/')

    for group_name, group_models in vector_models.items():
        logging.debug(f"Checking group: {group_name}")
        for model in group_models:
            logging.debug(f"Checking model: {model['repo_id']} / {model['name']}")
            if model['repo_id'] == repo_style_name or model['name'] in model_name:
                logging.debug(f"Found match! Using precision: {model['precision']}")
                return model['precision']
    logging.debug("No match found, defaulting to float32")
    return 'float32'

def get_appropriate_dtype(compute_device, use_half, model_native_precision):
    logging.debug(f"compute_device: {compute_device}")
    logging.debug(f"use_half: {use_half}")
    logging.debug(f"model_native_precision: {model_native_precision}")

    compute_device = compute_device.lower()
    model_native_precision = model_native_precision.lower()

    if compute_device == 'cpu':
        logging.debug("Using CPU, returning float32")
        return torch.float32

    cuda_available = torch.cuda.is_available()
    if cuda_available:
        cuda_capability = torch.cuda.get_device_capability()
        logging.debug(f"CUDA is available. Capability: {cuda_capability}")
    else:
        cuda_capability = (0, 0)
        logging.debug("CUDA is not available.")

    if model_native_precision == 'bfloat16':
        if use_half:
            if cuda_available:
                if cuda_capability[0] >= 8:
                    logging.debug("Model native precision is bfloat16, GPU supports it, returning bfloat16")
                    return torch.bfloat16
                else:
                    logging.debug("GPU doesn't support bfloat16, falling back to float16")
                    return torch.float16
            else:
                logging.debug("No CUDA available for bfloat16, falling back to float32")
                return torch.float32
        else:
            logging.debug("Half checkbox not checked for bfloat16 model, returning float32")
            return torch.float32

    elif model_native_precision == 'float16':
        if use_half:
            if cuda_available:
                logging.debug("Model native precision is float16 and CUDA is available, returning float16")
                return torch.float16
            else:
                logging.debug("Model native precision is float16 but CUDA is not available, returning float32")
                return torch.float32
        else:
            logging.debug("Half checkbox not checked for float16 model, returning float32")
            return torch.float32

    elif model_native_precision == 'float32':
        if not use_half:
            logging.debug("Model is float32 and use_half is False, returning float32")
            return torch.float32
        else:
            if cuda_available:
                if cuda_capability[0] >= 8:
                    logging.debug("Using bfloat16 due to Ampere+ GPU")
                    return torch.bfloat16
                else:
                    logging.debug("Using float16 due to pre-Ampere GPU")
                    return torch.float16
            else:
                logging.debug("No CUDA available, returning float32")
                return torch.float32

    else:
        logging.debug(f"Unrecognized precision '{model_native_precision}', returning float32")
        return torch.float32


def format_citations(metadata_list):
    def group_metadata(metadata_list):
        grouped = {}
        for metadata in metadata_list:
            file_path = metadata['file_path']
            grouped.setdefault(file_path, {
                'name': Path(file_path).name,
                'scores': [],
                'pages': set(),
                'file_type': metadata.get('file_type', '')
            })
            grouped[file_path]['scores'].append(metadata['similarity_score'])
            if grouped[file_path]['file_type'] == '.pdf':
                page_number = metadata.get('page_number')
                if page_number is not None:
                    grouped[file_path]['pages'].add(page_number)
        return grouped

    def format_pages(pages):
        if not pages:
            return ''
        sorted_pages = sorted(pages)
        ranges = []
        start = prev = sorted_pages[0]
        for page in sorted_pages[1:]:
            if page == prev + 1:
                prev = page
            else:
                ranges.append((start, prev))
                start = prev = page
        ranges.append((start, prev))
        page_str = ', '.join(f"{s}-{e}" if s != e else f"{s}" for s, e in ranges)
        return f'<span style="color:#666;"> p.{page_str}</span>'

    def create_citation(data, file_path):
        min_score = min(data['scores'])
        max_score = max(data['scores'])
        score_range = f"{min_score:.4f}" if min_score == max_score else f"{min_score:.4f}-{max_score:.4f}"
        pages_html = format_pages(data['pages']) if data['file_type'] == '.pdf' else ''
        citation = (
            f'<a href="file:{file_path}" style="color:#DAA520;text-decoration:none;">{data["name"]}</a>'
            f'<span style="color:#808080;font-size:0.9em;"> ['
            f'<span style="color:#4CAF50;">{score_range}</span>]'
            f'{pages_html}'
            f'</span>'
        )
        return min_score, citation

    grouped_citations = group_metadata(metadata_list)
    citations_with_scores = [create_citation(data, file_path) for file_path, data in grouped_citations.items()]
    sorted_citations = [citation for _, citation in sorted(citations_with_scores)]
    list_items = "".join(f"<li>{citation}</li>" for citation in sorted_citations)

    return f"<ol>{list_items}</ol>"


def save_config_atomically(config_data, config_path, **dump_kwargs):
    config_path = Path(config_path)
    tmp = config_path.with_name(config_path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        yaml.safe_dump(config_data, f, **dump_kwargs)
    os.replace(tmp, config_path)

def check_preconditions_for_submit_question(script_dir):
    config_path = script_dir / 'config.yaml'

    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    database_to_search = config.get('database', {}).get('database_to_search')

    vector_db_subdir = script_dir / "Vector_DB" / str(database_to_search) if database_to_search else None

    return True, ""

def my_cprint(*args, **kwargs):
    filename = os.path.basename(sys._getframe(1).f_code.co_filename)
    modified_message = f"{args[0]}"
    kwargs['flush'] = True
    cprint(modified_message, *args[1:], **kwargs)


def has_bfloat16_support():
   logging.debug("Checking bfloat16 support")

   if not torch.cuda.is_available():
       logging.debug("CUDA not available, bfloat16 not supported")
       return False

   capability = torch.cuda.get_device_capability()
   logging.debug(f"CUDA compute capability: {capability}")

   has_support = capability >= (8, 0)
   logging.debug(f"bfloat16 {'supported' if has_support else 'not supported'}")
   return has_support

def cuda_usable():
    return torch.cuda.is_available()

def runs_on_this_hardware(model_info):
    return not (model_info or {}).get("requires_cuda", False) or cuda_usable()

def fallback_if_unavailable(saved_key, registry, default_key):
    if saved_key in registry and runs_on_this_hardware(registry[saved_key]):
        return saved_key
    return default_key


def usable_whisper_models():
    from core.constants import WHISPER_MODELS

    cuda_available = torch.cuda.is_available()
    bfloat16_supported = has_bfloat16_support()

    usable = []
    for model_name, model_info in WHISPER_MODELS.items():
        precision = model_info['precision']
        if precision == 'float32':
            usable.append(model_name)
        elif precision == 'bfloat16' and bfloat16_supported:
            usable.append(model_name)
        elif precision == 'float16' and cuda_available:
            usable.append(model_name)
    return usable


def set_logging_level():
    library_levels = {
        "accelerate": logging.WARNING,
        "bitsandbytes": logging.WARNING,
        "ctranslate2": logging.WARNING,
        "datasets": logging.WARNING,
        "einops": logging.WARNING,
        "einx": logging.WARNING,
        "huggingface-hub": logging.WARNING,
        "numpy": logging.WARNING,
        "openai": logging.WARNING,
        "openai-whisper": logging.WARNING,
        "optimum": logging.WARNING,
        "pillow": logging.WARNING,
        "requests": logging.WARNING,
        "sentence-transformers": logging.WARNING,
        "sounddevice": logging.WARNING,
        "speechbrain": logging.WARNING,
        "sympy": logging.WARNING,
        "tiledb": logging.WARNING,
        "tiledb-cloud": logging.WARNING,
        "tiledb-vector-search": logging.WARNING,
        "timm": logging.WARNING,
        "tokenizers": logging.WARNING,
        "torch": logging.WARNING,
        "torchaudio": logging.WARNING,
        "torchvision": logging.WARNING,
        "transformers": logging.WARNING,
        "vector-quantize-pytorch": logging.WARNING,
        "vocos": logging.WARNING
    }

    for lib, level in library_levels.items():
        logging.getLogger(lib).setLevel(level)

def prepare_long_path(base_path: str, filename: str) -> str:
    base_path = os.path.normpath(base_path)
    full_path = os.path.join(base_path, filename)

    if os.name == 'nt' and len(full_path) > 255:
        full_path = "\\\\?\\" + os.path.abspath(full_path)

    return full_path


def get_embedding_batch_size(model_name: str, compute_device: str) -> int:
    if compute_device.lower() == 'cpu':
        return 2

    batch_size_mapping = {
        'harrier-oss-v1-0.6b': 4,
        'harrier-oss-v1-270m': 10,
        'Jasper-Token-Compression-600M': 4,
        'Yuan-embedding-2.0-en': 4,
        'F2LLM-v2-1.7B': 4,
        'F2LLM-v2-4B': 3,
        'geevec-embeddings-1.0-lite': 4,
        'Qwen3-Embedding-8B': 2,
        'Qwen3-Embedding-4B': 3,
        'Qwen3-Embedding-0.6B': 4,
        'Octen-Embedding-8B': 2,
        'Octen-Embedding-4B': 3,
        'Octen-Embedding-0.6B': 4,
        'e5-base': 6,
        'e5-large': 7,
        'bge-large-en-v1.5': 6,
        'e5-small': 10,
        'gte-large': 12,
        'bge-small': 12,
        'bge-small-en-v1.5': 12,
        'bge-base-en-v1.5': 8,
        'gte-base': 14,
    }

    model_name_lower = model_name.lower()
    for key, value in batch_size_mapping.items():
        if key.lower() in model_name_lower:
            return value

    return 8


def quiet_transformers_loading_bars():
    from transformers.utils import logging as transformers_logging

    def _hook(factory, args, kwargs):
        if kwargs.get("desc") == "Loading weights":
            kwargs = {**kwargs, "disable": True}
        return factory(*args, **kwargs)

    transformers_logging.set_tqdm_hook(_hook)


def get_embedding_dtype_and_batch(
    compute_device: str,
    use_half: bool,
    model_native_precision: str,
    model_name: str,
    is_query: bool,
):
    dtype = get_appropriate_dtype(compute_device, use_half, model_native_precision)
    if dtype == torch.float16 and _is_fp16_unsafe(model_name):
        dtype = torch.float32
    batch = 1 if is_query else get_embedding_batch_size(model_name, compute_device)
    return dtype, batch


def configure_logging(level: str = "INFO"):
    root = logging.getLogger()
    if root.handlers:
        root.setLevel(level.upper())
        return
    root.setLevel(level.upper())
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    h.setFormatter(fmt)
    root.addHandler(h)


def _is_fp16_unsafe(embedding_model_name):
    from core.constants import VECTOR_MODELS
    repo_style_name = os.path.basename(embedding_model_name).replace('--', '/')
    return any(model.get('fp16_unsafe') for group_models in VECTOR_MODELS.values()
               for model in group_models if model['repo_id'] == repo_style_name)
