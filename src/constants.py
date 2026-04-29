priority_libs = {
    "cp311": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu124torch2.6.0cxx11abiFALSE-cp311-cp311-win_amd64.whl",
            "https://download.pytorch.org/whl/cu124/torch-2.6.0%2Bcu124-cp311-cp311-win_amd64.whl#sha256=6a1fb2714e9323f11edb6e8abf7aad5f79e45ad25c081cde87681a18d99c29eb",
            "https://download.pytorch.org/whl/cu124/torchvision-0.21.0%2Bcu124-cp311-cp311-win_amd64.whl#sha256=000a013584ad2304ab30496318145f284ac364622addb5ee3a5abd2769ba146f",
            "https://download.pytorch.org/whl/cu124/torchaudio-2.6.0%2Bcu124-cp311-cp311-win_amd64.whl#sha256=a25e146ce66ea9a6aed39008cc2001891bdf75253af479a4c32096678b2073b3",
            "triton-windows==3.2.0.post12",
            "git+https://github.com/shashikg/WhisperS2T.git@e7f7e6dbfdc7f3a39454feb9dd262fd3653add8c",
            "git+https://github.com/BBC-Esq/WhisperSpeech.git@795f60157136b0052b9a1f576e88803f7783ab1f",
            "xformers==0.0.29.post3",
            "nvidia-cuda-runtime-cu12==12.4.127",
            "nvidia-cublas-cu12==12.4.5.8",
            "nvidia-cuda-nvrtc-cu12==12.4.127",
            "nvidia-cuda-nvcc-cu12==12.4.131",
            "nvidia-cufft-cu12==11.2.1.3",
            "nvidia-cudnn-cu12==9.1.0.70",
            "nvidia-ml-py==12.570.86",
        ],
        "CPU": [
        ],
        "COMMON": [
            "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.8.0-tesseract-5.5.0/tesserocr-2.8.0-cp311-cp311-win_amd64.whl",
        ],
    },
    "cp312": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu124torch2.6.0cxx11abiFALSE-cp312-cp312-win_amd64.whl",
            "https://download.pytorch.org/whl/cu124/torch-2.6.0%2Bcu124-cp312-cp312-win_amd64.whl#sha256=3313061c1fec4c7310cf47944e84513dcd27b6173b72a349bb7ca68d0ee6e9c0",
            "https://download.pytorch.org/whl/cu124/torchvision-0.21.0%2Bcu124-cp312-cp312-win_amd64.whl#sha256=ec63c2ee792757492da40590e34b14f2fceda29050558c215f0c1f3b08149c0f",
            "https://download.pytorch.org/whl/cu124/torchaudio-2.6.0%2Bcu124-cp312-cp312-win_amd64.whl#sha256=004ff6bcee0ac78747253c09db67d281add4308a9b87a7bf1769da5914998639",
            "triton-windows==3.2.0.post12",
            "git+https://github.com/shashikg/WhisperS2T.git@e7f7e6dbfdc7f3a39454feb9dd262fd3653add8c",
            "git+https://github.com/BBC-Esq/WhisperSpeech.git@795f60157136b0052b9a1f576e88803f7783ab1f",
            "xformers==0.0.29.post3",
            "nvidia-cuda-runtime-cu12==12.4.127",
            "nvidia-cublas-cu12==12.4.5.8",
            "nvidia-cuda-nvrtc-cu12==12.4.127",
            "nvidia-cuda-nvcc-cu12==12.4.131",
            "nvidia-cufft-cu12==11.2.1.3",
            "nvidia-cudnn-cu12==9.1.0.70",
            "nvidia-ml-py==12.570.86",
        ],
        "CPU": [
        ],
        "COMMON": [
            "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.8.0-tesseract-5.5.0/tesserocr-2.8.0-cp312-cp312-win_amd64.whl",
        ]
    }
}

libs = [
    "accelerate==1.5.1",
    "aiofiles==24.1.0",
    "aiohappyeyeballs==2.6.1",
    "aiohttp==3.11.13",
    "aiosignal==1.3.2",
    "anndata==0.11.3",
    "annotated-types==0.7.0",
    "anyio==4.8.0",
    "array_api_compat==1.11.1",
    "async-timeout==5.0.1",
    "attrs==25.2.0",
    "av==14.2.0",
    "backoff==2.2.1",
    "beautifulsoup4==4.13.3",
    "bitsandbytes==0.45.3",
    "braceexpand==0.1.7",
    "certifi==2025.1.31",
    "cffi==1.17.1",
    "chardet==5.2.0",
    "charset-normalizer==3.4.1",
    "chattts==0.2.2",
    "click==8.1.8",
    "cloudpickle==3.1.1",
    "colorama==0.4.6",
    "coloredlogs==15.0.1",
    "contourpy==1.3.1",
    "cryptography==44.0.2",
    "ctranslate2==4.5.0",
    "cycler==0.12.1",
    "dataclasses-json==0.6.7",
    "datasets==3.3.2",
    "deepdiff==8.3.0",
    "Deprecated==1.2.18",
    "deprecation==2.1.0",
    "dill==0.3.8",
    "distro==1.9.0",
    "docx2txt==0.8",
    "einops==0.8.1",
    "einx==0.3.0",
    "emoji==2.14.1",
    "encodec==0.1.1",
    "et-xmlfile==2.0.0",
    "eval-type-backport==0.2.2",
    "fastcore==1.7.29",
    "fastprogress==1.0.3",
    "filetype==1.2.0",
    "filelock==3.17.0",
    "fonttools==4.56.0",
    "frozendict==2.4.6",
    "frozenlist==1.5.0",
    "fsspec==2024.9.0",
    "greenlet==3.1.1",
    "gTTS==2.5.4",
    "h11==0.14.0",
    "h5py==3.13.0",
    "html5lib==1.1",
    "httpcore==1.0.7",
    "httpx==0.28.1",
    "httpx-sse==0.4.0",
    "huggingface-hub==0.29.3",
    "humanfriendly==10.0",
    "HyperPyYAML==1.2.2",
    "idna==3.10",
    "img2pdf==0.6.0",
    "importlib_metadata==8.6.1",
    "Jinja2==3.1.6",
    "jiter==0.9.0",
    "joblib==1.4.2",
    "jsonpatch==1.33",
    "jsonpath-python==1.0.6",
    "jsonpointer==3.0.0",
    "kiwisolver==1.4.8",
    "langchain==0.3.20",
    "langchain-community==0.3.19",
    "langchain-core==0.3.44",
    "langchain-huggingface==0.1.2",
    "langchain-text-splitters==0.3.6",
    "langdetect==1.0.9",
    "langsmith==0.3.13",
    "llvmlite==0.44.0",
    "lxml==5.3.1",
    "Markdown==3.7",
    "markdown-it-py==3.0.0",
    "MarkupSafe==3.0.2",
    "marshmallow==3.26.1",
    "matplotlib==3.10.1",
    "mdurl==0.1.2",
    "more-itertools==10.6.0",
    "mpmath==1.3.0",
    "msg-parser==1.2.0",
    "multidict==6.1.0",
    "multiprocess==0.70.16",
    "mypy-extensions==1.0.0",
    "natsort==8.4.0",
    "nest-asyncio==1.6.0",
    "networkx==3.4.2",
    "nltk==3.9.1",
    "numba==0.61.0",
    "numpy==1.26.4",
    "ocrmypdf==16.10.0",
    "olefile==0.47",
    "openai==1.66.2",
    "openai-whisper==20240930",
    "openpyxl==3.1.5",
    "optimum==1.24.0",
    "ordered-set==4.1.0",
    "orderly-set==5.3.0",
    "orjson==3.10.15",
    "packaging==24.2",
    "pandas==2.2.3",
    "pdfminer.six==20240706",
    "pikepdf==9.5.2",
    "pillow==11.1.0",
    "pi-heif==0.21.0",
    "pipdeptree",
    "platformdirs==4.3.6",
    "pluggy==1.5.0",
    "propcache==0.3.0",
    "protobuf==5.29.3",
    "psutil==7.0.0",
    "pyarrow==19.0.1",
    "pybase16384==0.3.8",
    "pycparser==2.22",
    "pydantic==2.10.6",
    "pydantic_core==2.27.2",
    "pydantic-settings==2.7.1",
    "Pygments==2.19.1",
    "PyOpenGL==3.1.9",
    "PyOpenGL-accelerate==3.1.9",
    "pypandoc==1.15",
    "pyparsing==3.2.1",
    "pypdf==5.3.1",
    "pyreadline3==3.5.4",
    "python-dateutil==2.9.0.post0",
    "python-docx==1.1.2",
    "python-dotenv==1.0.1",
    "python-iso639==2025.2.18",
    "python-magic==0.4.27",
    "python-oxmsg==0.0.2",
    "pytz==2025.1",
    "PyYAML==6.0.2",
    "rapidfuzz==3.12.2",
    "regex==2024.11.6",
    "requests==2.32.3",
    "requests-toolbelt==1.0.0",
    "rich==13.9.4",
    "ruamel.yaml==0.18.10",
    "ruamel.yaml.clib==0.2.12",
    "safetensors==0.5.3",
    "scikit-learn==1.6.1",
    "scipy==1.15.2",
    "sentence-transformers==3.4.1",
    "sentencepiece==0.2.0",
    "six==1.17.0",
    "sniffio==1.3.1",
    "sounddevice==0.5.1",
    "soundfile==0.13.1",
    "soupsieve==2.6",
    "speechbrain==0.5.16",
    "SQLAlchemy==2.0.39",
    "sseclient-py==1.8.0",
    "sympy==1.13.1",
    "tabulate==0.9.0",
    "tblib==3.0.0",
    "tenacity==9.0.0",
    "termcolor==2.5.0",
    "tessdata==1.0.0",
    "tessdata.eng==1.0.0",
    "threadpoolctl==3.5.0",
    "tiktoken==0.9.0",
    "tiledb==0.33.5",
    "tiledb-cloud==0.13.0",
    "tiledb-vector-search==0.11.0",
    "timm==1.0.15",
    "tokenizers==0.21.0",
    "tqdm==4.67.1",
    "transformers==4.49.0",
    "typing-inspect==0.9.0",
    "typing_extensions==4.12.2",
    "unstructured-client==0.31.1",
    "tzdata==2025.1",
    "urllib3==2.3.0",
    "vector-quantize-pytorch==1.22.2",
    "vocos==0.1.0",
    "watchdog==6.0.0",
    "webdataset==0.2.111",
    "webencodings==0.5.1",
    "wrapt==1.17.2",
    "xlrd==2.0.1",
    "xxhash==3.5.0",
    "yarl==1.18.3",
    "zipp==3.21.0",
    "zstandard==0.23.0"
]

full_install_libs = [
    "PySide6==6.8.2.1",
    "pymupdf==1.25.3",
    "unstructured==0.17.0"
]

VECTOR_MODELS = {
    'Alibaba-NLP': [
        {
            'name': 'Alibaba-gte-base',
            'dimensions': 768,
            'max_sequence': 8192,
            'size_mb': 547,
            'repo_id': 'Alibaba-NLP/gte-base-en-v1.5',
            'cache_dir': 'Alibaba-NLP--gte-base-en-v1.5',
            'type': 'vector',
            'parameters': '137m',
            'precision': 'float32'
        },
        {
            'name': 'Alibaba-gte-modernbert-base',
            'dimensions': 768,
            'max_sequence': 8192,
            'size_mb': 298,
            'repo_id': 'Alibaba-NLP/gte-modernbert-base',
            'cache_dir': 'Alibaba-NLP--gte-modernbert-base',
            'type': 'vector',
            'parameters': '149m',
            'precision': 'float16'
        },
        {
            'name': 'Alibaba-gte-large',
            'dimensions': 1024,
            'max_sequence': 8192,
            'size_mb': 1740,
            'repo_id': 'Alibaba-NLP/gte-large-en-v1.5',
            'cache_dir': 'Alibaba-NLP--gte-large-en-v1.5',
            'type': 'vector',
            'parameters': '434m',
            'precision': 'float32'
        },
    ],
    'BAAI': [
        {
            'name': 'bge-small-en-v1.5',
            'dimensions': 384,
            'max_sequence': 512,
            'size_mb': 134,
            'repo_id': 'BAAI/bge-small-en-v1.5',
            'cache_dir': 'BAAI--bge-small-en-v1.5',
            'type': 'vector',
            'parameters': '33.4m',
            'precision': 'float32'
        },
        {
            'name': 'bge-base-en-v1.5',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 438,
            'repo_id': 'BAAI/bge-base-en-v1.5',
            'cache_dir': 'BAAI--bge-base-en-v1.5',
            'type': 'vector',
            'parameters': '109m',
            'precision': 'float32'
        },
        {
            'name': 'bge-large-en-v1.5',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 1340,
            'repo_id': 'BAAI/bge-large-en-v1.5',
            'cache_dir': 'BAAI--bge-large-en-v1.5',
            'type': 'vector',
            'parameters': '335m',
            'precision': 'float32'
        },
    ],
    'IBM': [
        {
            'name': 'Granite-30m-English',
            'dimensions': 384,
            'max_sequence': 512,
            'size_mb': 61,
            'repo_id': 'ibm-granite/granite-embedding-30m-english',
            'cache_dir': 'ibm-granite--granite-embedding-30m-english',
            'type': 'vector',
            'parameters': '30.3m',
            'precision': 'bfloat16'
        },
        {
            'name': 'Granite-125m-English',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 249,
            'repo_id': 'ibm-granite/granite-embedding-125m-english',
            'cache_dir': 'ibm-granite--granite-embedding-125m-english',
            'type': 'vector',
            'parameters': '125m',
            'precision': 'bfloat16'
        },
    ],
    'intfloat': [
        {
            'name': 'e5-small-v2',
            'dimensions': 384,
            'max_sequence': 512,
            'size_mb': 134,
            'repo_id': 'intfloat/e5-small-v2',
            'cache_dir': 'intfloat--e5-small-v2',
            'type': 'vector',
            'parameters': '33.4m',
            'precision': 'float32'
        },
        {
            'name': 'e5-base-v2',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 438,
            'repo_id': 'intfloat/e5-base-v2',
            'cache_dir': 'intfloat--e5-base-v2',
            'type': 'vector',
            'parameters': '109m',
            'precision': 'float32'
        },
        {
            'name': 'e5-large-v2',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 1340,
            'repo_id': 'intfloat/e5-large-v2',
            'cache_dir': 'intfloat--e5-large-v2',
            'type': 'vector',
            'parameters': '335m',
            'precision': 'float32'
        },
    ],
    'NovaSearch': [
        {
            'name': 'stella_en_1.5B_v5',
            'dimensions': 1024,
            'max_sequence': 131072,
            'size_mb': 6170,
            'repo_id': 'NovaSearch/stella_en_1.5B_v5',
            'cache_dir': 'NovaSearch--stella_en_1.5B_v5',
            'type': 'vector',
            'parameters': '1540m',
            'precision': 'float32'
        },
        {
            'name': 'stella_en_400M_v5',
            'dimensions': 1024,
            'max_sequence': 8192,
            'size_mb': 1740,
            'repo_id': 'NovaSearch/stella_en_400M_v5',
            'cache_dir': 'NovaSearch--stella_en_400M_v5',
            'type': 'vector',
            'parameters': '435m',
            'precision': 'float32'
        },
    ],
    'Snowflake': [
        {
            'name': 'arctic-embed-m-v2.0',
            'dimensions': 768,
            'max_sequence': 8192,
            'size_mb': 1220,
            'repo_id': 'Snowflake/snowflake-arctic-embed-m-v2.0',
            'cache_dir': 'Snowflake--snowflake-arctic-embed-m-v2.0',
            'type': 'vector',
            'parameters': '305m',
            'precision': 'float32'
        },
        {
            'name': 'arctic-embed-l-v2.0',
            'dimensions': 1024,
            'max_sequence': 8192,
            'size_mb': 2270,
            'repo_id': 'Snowflake/snowflake-arctic-embed-l-v2.0',
            'cache_dir': 'Snowflake--snowflake-arctic-embed-l-v2.0',
            'type': 'vector',
            'parameters': '568m',
            'precision': 'float32'
        },
    ],
}

VISION_MODELS = {
    'InternVL2.5 - 1b': {
        'precision': 'bfloat16',
        'quant': 'n/a',
        'size': '1b',
        'repo_id': 'ctranslate2-4you/InternVL2_5-1B',
        'cache_dir': 'ctranslate2-4you--InternVL2_5-1B',
        'requires_cuda': True,
        'vram': '2.4 GB',
        'loader': 'loader_internvl2_5'
    },
    'Ovis2 - 1b': {
        'precision': 'bfloat16',
        'quant': 'n/a',
        'size': '1b',
        'repo_id': 'AIDC-AI/Ovis2-1B',
        'cache_dir': 'AIDC-AI--Ovis2-1B',
        'requires_cuda': True,
        'vram': '2.4 GB',
        'loader': 'loader_ovis'
    },
    'Florence-2-base': {
        'precision': 'autoselect',
        'quant': 'n/a',
        'size': '232m',
        'repo_id': 'microsoft/Florence-2-base',
        'cache_dir': 'microsoft--Florence-2-base',
        'requires_cuda': False,
        'vram': '2.6 GB',
        'loader': 'loader_florence2'
    },
    'InternVL2.5 - 4b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '4b',
        'repo_id': 'ctranslate2-4you/InternVL2_5-4B',
        'cache_dir': 'ctranslate2-4you--InternVL2_5-4B',
        'requires_cuda': True,
        'vram': '3.2 GB',
        'loader': 'loader_internvl2_5'
    },
    'Granite Vision - 2b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '2b',
        'repo_id': 'ibm-granite/granite-vision-3.2-2b',
        'cache_dir': 'ibm-granite--granite-vision-3.2-2b',
        'requires_cuda': True,
        'vram': '4.1 GB',
        'loader': 'loader_granite'
    },
    'Florence-2-large': {
        'precision': 'autoselect',
        'quant': 'n/a',
        'size': '770m',
        'repo_id': 'microsoft/Florence-2-large',
        'cache_dir': 'microsoft--Florence-2-large',
        'requires_cuda': False,
        'vram': '5.3 GB',
        'loader': 'loader_florence2'
    },
    'Ovis2 - 2b': {
        'precision': 'bfloat16',
        'quant': 'n/a',
        'size': '2b',
        'repo_id': 'AIDC-AI/Ovis2-2B',
        'cache_dir': 'AIDC-AI--Ovis2-2B',
        'requires_cuda': True,
        'vram': '2.4 GB',
        'loader': 'loader_ovis'
    },
    'Qwen VL - 3b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '3b',
        'repo_id': 'Qwen/Qwen2.5-VL-3B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-VL-3B-Instruct',
        'requires_cuda': True,
        'vram': '6.3 GB',
        'loader': 'loader_qwenvl'
    },
    'Qwen VL - 7b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '7b',
        'repo_id': 'Qwen/Qwen2.5-VL-7B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-VL-7B-Instruct',
        'requires_cuda': True,
        'vram': '9.6 GB',
        'loader': 'loader_qwenvl'
    },
    'THUDM glm4v - 9b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '9b',
        'repo_id': 'ctranslate2-4you/glm-4v-9b',
        'cache_dir': 'ctranslate2-4you--glm-4v-9b',
        'requires_cuda': True,
        'vram': '10.5 GB',
        'loader': 'loader_glmv4'
    },
    'Molmo-D-0924 - 8b': {
        'precision': 'bfloat16',
        'quant': '4-bit',
        'size': '8b',
        'repo_id': 'ctranslate2-4you/molmo-7B-D-0924-bnb-4bit',
        'cache_dir': 'ctranslate2-4you--molmo-7B-D-0924-bnb-4bit',
        'requires_cuda': True,
        'vram': '10.5 GB',
        'loader': 'loader_molmo'
    },
}

WHISPER_MODELS = {
    'Distil Whisper large-v3 - float32': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float32',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper large-v3 - bfloat16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-bfloat16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper large-v3 - float16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Whisper large-v3 - float32': {
        'name': 'Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float32',
        'cps': 85,
        'optimal_batch_size': 2,
        'vram': '5.5 GB'
    },
    'Whisper large-v3 - bfloat16': {
        'name': 'Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-bfloat16',
        'cps': 95,
        'optimal_batch_size': 3,
        'vram': '3.8 GB'
    },
    'Whisper large-v3 - float16': {
        'name': 'Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float16',
        'cps': 100,
        'optimal_batch_size': 3,
        'vram': '3.3 GB'
    },
    'Distil Whisper medium.en - float32': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float32',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper medium.en - bfloat16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-bfloat16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper medium.en - float16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Whisper medium.en - float32': {
        'name': 'Whisper medium.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float32',
        'cps': 130,
        'optimal_batch_size': 6,
        'vram': '2.5 GB'
    },
    'Whisper medium.en - bfloat16': {
        'name': 'Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-bfloat16',
        'cps': 140,
        'optimal_batch_size': 7,
        'vram': '2.0 GB'
    },
    'Whisper medium.en - float16': {
        'name': 'Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float16',
        'cps': 145,
        'optimal_batch_size': 7,
        'vram': '1.8 GB'
    },
    'Distil Whisper small.en - float32': {
        'name': 'Distil Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float32',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper small.en - bfloat16': {
        'name': 'Distil Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-bfloat16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Distil Whisper small.en - float16': {
        'name': 'Distil Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float16',
        'cps': 160,
        'optimal_batch_size': 4,
        'vram': '3.0 GB'
    },
    'Whisper small.en - float32': {
        'name': 'Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float32',
        'cps': 180,
        'optimal_batch_size': 14,
        'vram': '1.5 GB'
    },
    'Whisper small.en - bfloat16': {
        'name': 'Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-bfloat16',
        'cps': 190,
        'optimal_batch_size': 15,
        'vram': '1.2 GB'
    },
    'Whisper small.en - float16': {
        'name': 'Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float16',
        'cps': 195,
        'optimal_batch_size': 15,
        'vram': '1.1 GB'
    },
    'Whisper base.en - float32': {
        'name': 'Whisper base.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float32',
        'cps': 230,
        'optimal_batch_size': 22,
        'vram': '1.0 GB'
    },
    'Whisper base.en - bfloat16': {
        'name': 'Whisper base.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-bfloat16',
        'cps': 240,
        'optimal_batch_size': 23,
        'vram': '0.85 GB'
    },
    'Whisper base.en - float16': {
        'name': 'Whisper base.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float16',
        'cps': 245,
        'optimal_batch_size': 23,
        'vram': '0.8 GB'
    },
    'Whisper tiny.en - float32': {
        'name': 'Whisper tiny.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float32',
        'cps': 280,
        'optimal_batch_size': 30,
        'vram': '0.7 GB'
    },
    'Whisper tiny.en - bfloat16': {
        'name': 'Whisper tiny.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-bfloat16',
        'cps': 290,
        'optimal_batch_size': 31,
        'vram': '0.6 GB'
    },
    'Whisper tiny.en - float16': {
        'name': 'Whisper tiny.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float16',
        'cps': 295,
        'optimal_batch_size': 31,
        'vram': '0.55 GB'
    },
}

DOCUMENT_LOADERS = {
    ".pdf": "CustomPyMuPDFLoader",
    ".docx": "Docx2txtLoader",
    ".txt": "TextLoader",
    ".enex": "EverNoteLoader",
    ".epub": "UnstructuredEPubLoader",
    ".eml": "UnstructuredEmailLoader",
    ".msg": "UnstructuredEmailLoader",
    ".csv": "CSVLoader",
    ".xls": "UnstructuredExcelLoader",
    ".xlsx": "UnstructuredExcelLoader",
    ".xlsm": "UnstructuredExcelLoader",
    ".rtf": "UnstructuredRTFLoader",
    ".odt": "UnstructuredODTLoader",
    ".md": "UnstructuredMarkdownLoader",
    ".html": "BSHTMLLoader",
}

TOOLTIPS = {
    "AUDIO_FILE_SELECT": "Select an audio file. Supports various audio formats.",
    "CHOOSE_FILES": "Select documents to add to the database. Remember to transcribe audio files in the Tools tab first.",
    "CHUNK_OVERLAP": "Characters shared between chunks. Set to 25-50% of chunk size.",
    "CHUNK_SIZE": (
        "<html><body>"
        "Upper limit (in characters, not tokens) that a chunk can be after being split.  Make sure that it falls within"
        "the Max Sequence of the embedding model being used, which is measured in tokens (not characters), remembering that"
        "approximately 3-4 characters = 1 token."
        "</body></html>"
    ),
    "CONTEXTS": "Maximum number of chunks (aka contexts) to return.",
    "COPY_RESPONSE": "Copy the chunks (if chunks only is checked) or model's response to the clipboard.",
    "CREATE_DEVICE_DB": "Choose 'cpu' or 'cuda'. Use 'cuda' if available.",
    "CREATE_DEVICE_QUERY": "Choose 'cpu' or 'cuda'. 'cpu' recommended to conserve VRAM.",
    "CREATE_VECTOR_DB": "Creates a new vector database.",
    "DATABASE_NAME_INPUT": "Enter a unique database name. Use only lowercase letters, numbers, underscores, and hyphens.",
    "DATABASE_SELECT": "Vector database that will be queried.",
    "DOWNLOAD_MODEL": "Download the selected vector model.",
    "EJECT_LOCAL_MODEL": "Unload the current local model from memory.",
    "FILE_TYPE_FILTER": "Only allows chunks that originate from certain file types.",
    "HALF_PRECISION": "Uses bfloat16/float16 for 2x speedup. Requires a GPU.",
    "LOCAL_MODEL_SELECT": "Select a local model for generating responses.",
    "MODEL_BACKEND_SELECT": "Choose the backend for the large language model response.",
    "PORT": "Must match the port used in LM Studio.",
    "QUESTION_INPUT": "Type your question here or use the voice recorder.",
    "RESTORE_CONFIG": "Restores original config.yaml. May require manual database cleanup.",
    "RESTORE_DATABASE": "Restores backed-up databases. Use with caution.",
    "SEARCH_TERM_FILTER": "Removes chunks without exact term. Case-insensitive.",
    "SELECT_VECTOR_MODEL": "Choose the vector model for text embedding.",
    "SIMILARITY": "Relevance threshold for chunks. 0-1, higher returns more. Don't use 1.",
    "SPEAK_RESPONSE": "Speak the response from the large language model using text-to-speech.",
    "SHOW_THINKING_CHECKBOX": "If checked, show the model's internal thought process.  Only applies to models like Deepseek's R1 and it will be disregarded if not applicable.",
    "TRANSCRIBE_BUTTON": "Start transcription.",
    "TTS_MODEL": "Choose TTS model. Bark offers customization, Google requires internet.",
    "VECTOR_MODEL_DIMENSIONS": "Higher dimensions captures more nuance but requires more processing time.",
    "VECTOR_MODEL_DOWNLOADED": "Whether the model has been downloaded.",
    "VECTOR_MODEL_LINK": "Huggingface link.",
    "VECTOR_MODEL_MAX_SEQUENCE": "Number of tokens the model can process at once. Different from the Chunk Size setting, which is in characters.",
    "VECTOR_MODEL_NAME": "The name of the vector model.",
    "VECTOR_MODEL_PARAMETERS": "The number of internal weights and biases that the model learns and adjusts during training.",
    "VECTOR_MODEL_PRECISION": (
        "<html>"
        "<body>"
        "<p style='font-size: 14px; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-bottom: 10px;'>"
        "<b>The precision ultimately used depends on your setup:</b></p>"
        "<table style='border-collapse: collapse; width: 100%; font-size: 12px; color: #34495e;'>"
        "<thead>"
        "<tr style='background-color: #ecf0f1; text-align: left;'>"
        "<th style='border: 1px solid #bdc3c7; padding: 8px;'>Compute Device</th>"
        "<th style='border: 1px solid #bdc3c7; padding: 8px;'>Embedding Model Precision</th>"
        "<th style='border: 1px solid #bdc3c7; padding: 8px;'>'Half' Checked?</th>"
        "<th style='border: 1px solid #bdc3c7; padding: 8px;'>Precision Ultimately Used</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        "<tr>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>CPU</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>Any</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>Either</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'><code>float32</code></td>"
        "</tr>"
        "<tr style='background-color: #ecf0f1;'>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>CUDA</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>float16</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>Yes</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'><code>float16</code></td>"
        "</tr>"
        "<tr>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>CUDA</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>bfloat16</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>Yes</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>"
        "<code>bfloat16</code> (if CUDA capability &ge; 8.0) or <code>float16</code></td>"
        "</tr>"
        "<tr style='background-color: #ecf0f1;'>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>CUDA</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>float32</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>No</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'><code>float32</code></td>"
        "</tr>"
        "<tr>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>CUDA</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>float32</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>Yes</td>"
        "<td style='border: 1px solid #bdc3c7; padding: 8px;'>"
        "<code>bfloat16</code> (if CUDA capability &ge; 8.0) or <code>float16</code>"
        "</td>"
        "</tr>"
        "</tbody>"
        "</table>"
        "</body>"
        "</html>"
    ),
    "VECTOR_MODEL_SELECT": "Choose a vector model to download.",
    "VECTOR_MODEL_SIZE": "Size on disk.",
    "VISION_MODEL": "Select vision model for image processing. Test before bulk processing.",
    "VOICE_RECORDER": "Click to start recording, speak your question, then click again to stop recording.",
    "WHISPER_BATCH_SIZE": "Batch size for transcription. See the User Guid for optimal values.",
    "WHISPER_MODEL_SELECT": "Distil models use ~ 70% VRAM of their non-Distil equivalents with little quality loss."
}

system_message = "You are a helpful person who clearly and directly answers questions in a succinct fashion based on contexts provided to you. If you cannot find the answer within the contexts simply tell me that the contexts do not provide an answer. However, if the contexts partially address my question I still want you to answer based on what the contexts say and then briefly summarize the parts of my question that the contexts didn't provide an answer."
rag_string = "Here are the contexts to base your answer on.  However, I need to reiterate that I only want you to base your response on these contexts and do not use outside knowledge that you may have been trained with."
