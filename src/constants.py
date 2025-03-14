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
            # CPU only libraries would go here
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
            # CPU only libraries would go here
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
    "aiohttp==3.11.13", # langchain libraries require <4
    "aiosignal==1.3.2", # only required by aiohttp
    "anndata==0.11.3",
    "annotated-types==0.7.0",
    "anyio==4.8.0",
    "array_api_compat==1.11.1", # only anndata requires
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
    "charset-normalizer==3.4.1", # requests requires <4
    "chattts==0.2.2",
    "click==8.1.8",
    "cloudpickle==3.1.1", # only required by tiledb-cloud and 3+ is only supported by tiledb-cloud 0.13+
    "colorama==0.4.6",
    "coloredlogs==15.0.1",
    "contourpy==1.3.1", # onlyk required by matplotlib
    "cryptography==44.0.2", # only required by unstructured library
    "ctranslate2==4.5.0",
    "cycler==0.12.1",
    "dataclasses-json==0.6.7",
    "datasets==3.3.2",
    "deepdiff==8.3.0", # required by unstructured
    "Deprecated==1.2.18", # only needed by pikepdf
    "deprecation==2.1.0", # only needed by ocrmypdf
    "dill==0.3.8", # datasets 3.2.0 requires <0.3.9; multiprocess 0.70.16 requires >=0.3.8
    "distro==1.9.0",
    "docx2txt==0.8",
    "einops==0.8.1",
    "einx==0.3.0",
    "emoji==2.14.1",
    "encodec==0.1.1",
    "et-xmlfile==2.0.0", # openpyxl requires; caution...openpyxl 3.1.5 (6/28/2024) predates et-xmlfile 2.0.0 (10/25/2024)
    "eval-type-backport==0.2.2", # only required by unstructured
    "fastcore==1.7.29", # only required by whisperspeech
    "fastprogress==1.0.3", # only required by whisperspeech
    "filetype==1.2.0",
    "filelock==3.17.0",
    "fonttools==4.56.0", # only required by matplotlib
    "frozendict==2.4.6",
    "frozenlist==1.5.0",
    "fsspec==2024.9.0", # datasets 3.2.0 requires <=2024.9.0
    "greenlet==3.1.1",
    "gTTS==2.5.4",
    "h11==0.14.0",
    "h5py==3.13.0",
    "html5lib==1.1", # only required by unstructured
    "httpcore==1.0.7",
    "httpx==0.28.1",
    "httpx-sse==0.4.0",
    "huggingface-hub==0.29.3", # tokenizers 0.20.3 requires >=0.16.4,<1.0
    "humanfriendly==10.0",
    "HyperPyYAML==1.2.2",
    "idna==3.10",
    "img2pdf==0.6.0",
    "importlib_metadata==8.6.1",
    "Jinja2==3.1.6",
    "jiter==0.9.0", # required by openai newer versions
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
    "llvmlite==0.44.0", # only required by numba
    "lxml==5.3.1",
    "Markdown==3.7",
    "markdown-it-py==3.0.0",
    "MarkupSafe==3.0.2",
    "marshmallow==3.26.1",
    "matplotlib==3.10.1", # uniquely requires pyparsing==3.1.2 cycler==0.12.1 kiwisolver==1.4.5
    "mdurl==0.1.2",
    "more-itertools==10.6.0",
    "mpmath==1.3.0", # sympy 1.13.1 requires less than 1.4
    "msg-parser==1.2.0",
    "multidict==6.1.0",
    "multiprocess==0.70.16", # datasets 3.2.0 requires <0.70.17
    "mypy-extensions==1.0.0",
    "natsort==8.4.0",
    "nest-asyncio==1.6.0",
    "networkx==3.4.2",
    "nltk==3.9.1", # not higher; gives unexplained error
    "numba==0.61.0", # only required by openai-whisper
    "numpy==1.26.4", # langchain libraries <2; numba <2.1; scipy <2.3; chattts <2.0.0
    "ocrmypdf==16.10.0",
    "olefile==0.47",
    "openai==1.66.2", # only required by chat_lm_studio.py script and whispers2t (if using openai vanilla backend)
    "openai-whisper==20240930", # only required by whisper_s2t (if using openai vanilla backend)
    "openpyxl==3.1.5",
    "optimum==1.24.0",
    "ordered-set==4.1.0",
    "orderly-set==5.3.0", # deepdiff 8.2.0 requires orderly-set=5.3.0,<6
    "orjson==3.10.15",
    "packaging==24.2",
    "pandas==2.2.3",
    "pdfminer.six==20240706", # only needed by ocrmypdf
    "pikepdf==9.5.2", # only needed by ocrmypdf
    "pillow==11.1.0",
    "pi-heif==0.21.0", # only needed by ocrmypdf, but not for my usage of ocrmypdf
    "pipdeptree",
    "platformdirs==4.3.6",
    "pluggy==1.5.0", # only needed by ocrmypdf
    "propcache==0.3.0",
    "protobuf==5.29.3",
    "psutil==7.0.0",
    "pyarrow==19.0.1",
    "pybase16384==0.3.8", # only required by chattts
    "pycparser==2.22",
    "pydantic==2.10.6",
    "pydantic_core==2.27.2", # pydantic 2.10.6 requires pydantic_core==2.27.2
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
    "python-oxmsg==0.0.2", # only required by unstructured library
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
    "SQLAlchemy==2.0.39", # langchain and langchain-community require less than 3.0.0
    "sseclient-py==1.8.0", # only required by Kobold
    "sympy==1.13.1", # torch 2.6.0 requires sympy==1.13.1
    "tabulate==0.9.0",
    "tblib==3.0.0", # only tiledb-cloud requires
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
    "urllib3==2.3.0", # requests 2.32.3 requires <3
    "vector-quantize-pytorch==1.22.2",
    "vocos==0.1.0",
    "watchdog==6.0.0",
    "webdataset==0.2.111", # required by all TTS libraries
    "webencodings==0.5.1", # only required by html5lib
    "wrapt==1.17.2",
    "xlrd==2.0.1",
    "xxhash==3.5.0",
    "yarl==1.18.3", # aiohttp requires <2
    "zipp==3.21.0",
    "zstandard==0.23.0" # only required by langsmith 3+
]

full_install_libs = [
    "PySide6==6.8.2.1",
    "pymupdf==1.25.3",
    "unstructured==0.17.0"
]

CHAT_MODELS = {
    'Qwen - 1.5b': {
        'model': 'Qwen - 1.5b',
        'repo_id': 'Qwen/Qwen2.5-1.5B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-1.5B-Instruct',
        'cps': 261.31,
        'context_length': 32768,
        'vram': 1749.97,
        'function': 'Qwen_1_5b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Qwen Coder - 1.5b': {
        'model': 'Qwen Coder - 1.5b',
        'repo_id': 'Qwen/Qwen2.5-Coder-1.5B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-Coder-1.5B-Instruct',
        'cps': 236.32,
        'context_length': 4096,
        'vram': 1742.12,
        'function': 'QwenCoder_1_5b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Granite - 2b': {
        'model': 'Granite - 2b',
        'repo_id': 'ibm-granite/granite-3.2-2b-instruct',
        'cache_dir': 'ibm-granite--granite-3.2-2b-instruct',
        'cps': 128.11,
        'context_length': 8192,
        'vram': 2292.18,
        'function': 'Granite_2b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Zephyr - 1.6b': {
        'model': 'Zephyr - 1.6b',
        'repo_id': 'stabilityai/stablelm-2-zephyr-1_6b',
        'cache_dir': 'stabilityai--stablelm-2-zephyr-1_6b',
        'cps': 375.77,
        'context_length': 4096,
        'vram': 2233.45,
        'function': 'Zephyr_1_6B',
        'precision': 'float16', # doesn't have a float32 version
        'gated': False,
    },
    'Zephyr - 3b': {
        'model': 'Zephyr - 3b',
        'repo_id': 'stabilityai/stablelm-zephyr-3b',
        'cache_dir': 'stabilityai--stablelm-zephyr-3b',
        'cps': 293.68,
        'context_length': 4096,
        'vram': 2733.85,
        'function': 'Zephyr_3B',
        'precision': 'bfloat16', # created float32 version
        'gated': False,
    },
    'Exaone - 2.4b': {
        'model': 'Exaone - 2.4b',
        'repo_id': 'LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct',
        'cache_dir': 'LGAI-EXAONE--EXAONE-3.5-2.4B-Instruct',
        'cps': 224.08,
        'context_length': 32768,
        'vram': 2821.06,
        'function': 'Exaone_2_4b',
        # 'precision': 'float32',
        'gated': False,
    },
    'Qwen Coder - 3b': {
        'model': 'Qwen Coder - 3b',
        'repo_id': 'Qwen/Qwen2.5-Coder-3B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-Coder-3B-Instruct',
        'cps': 198.99,
        'context_length': 32768,
        'vram': 2860.01,
        'function': 'QwenCoder_3b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Granite - 8b': {
        'model': 'Granite - 8b',
        'repo_id': 'ibm-granite/granite-3.2-8b-instruct',
        'cache_dir': 'ibm-granite--granite-3.2-8b-instruct',
        'cps': 137.73,
        'context_length': 8192,
        'vram': 5291.93,
        'function': 'Granite_8b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Deepseek R1 - 7b': {
        'model': 'Deepseek R1 - 7b',
        'repo_id': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
        'cache_dir': 'deepseek-ai--DeepSeek-R1-Distill-Qwen-7B',
        'cps': 40.35,
        'context_length': 8192,
        'vram': 6466.80,
        'function': 'DeepseekR1_7b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Exaone - 7.8b': {
        'model': 'Exaone - 7.8b',
        'repo_id': 'LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct',
        'cache_dir': 'LGAI-EXAONE--EXAONE-3.5-7.8B-Instruct',
        'cps': 187.24,
        'context_length': 32768,
        'vram': 6281.91,
        'function': 'Exaone_7_8b',
        # 'precision': 'float32',
        'gated': False,
    },
    'Qwen Coder - 7b': {
        'model': 'Qwen Coder - 7b',
        'repo_id': 'Qwen/Qwen2.5-Coder-7B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-Coder-7B-Instruct',
        'cps': 219.55,
        'context_length': 4096,
        'vram': 6760.18,
        'function': 'QwenCoder_7b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'InternLM 3 - 8b': {
        'model': 'InternLM 3 - 8b',
        'repo_id': 'internlm/internlm3-8b-instruct',
        'cache_dir': 'internlm--internlm3-8b-instruct',
        'cps': 134.69,
        'context_length': 8192,
        'vram': 6802.62,
        'function': 'Internlm3',
        'precision': 'bfloat16',
        'gated': False,
    },
    'OLMo 2 - 13b': {
        'model': 'OLMo 2 - 13b',
        'repo_id': 'allenai/OLMo-2-1124-13B-Instruct',
        'cache_dir': 'allenai--OLMo-2-1124-13B-Instruct',
        'cps': 179.76,
        'context_length': 8192,
        'vram': 9849.80,
        'function': 'OLMo2_13b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Deepseek R1 - 14b': {
        'model': 'Deepseek R1 - 14b',
        'repo_id': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B',
        'cache_dir': 'deepseek-ai--DeepSeek-R1-Distill-Qwen-14B',
        'cps': 29.64,
        'context_length': 8192,
        'vram': 10892.89,
        'function': 'DeepseekR1_14b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Qwen Coder - 14b': {
        'model': 'Qwen Coder - 14b',
        'repo_id': 'Qwen/Qwen2.5-Coder-14B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-Coder-14B-Instruct',
        'cps': 144.76,
        'context_length': 32768,
        'vram': 11029.87,
        'function': 'QwenCoder_14b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Qwen - 14b': {
        'model': 'Qwen - 14b',
        'repo_id': 'Qwen/Qwen2.5-14B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-14B-Instruct',
        'cps': 139.26,
        'context_length': 8192,
        'vram': 11168.49,
        'function': 'Qwen_14b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Mistral Small 3 - 24b': {
        'model': 'Mistral Small 3 - 24b',
        'repo_id': 'mistralai/Mistral-Small-24B-Instruct-2501',
        'cache_dir': 'mistralai--Mistral-Small-24B-Instruct-2501',
        'cps': 98.33,
        'context_length': 32768,
        'vram': 13723.65,
        'function': 'Mistral_Small_24b',
        'precision': 'bfloat16',
        'gated': True,
    },
    'QwQ - 32b': {
        'model': 'QwQ - 32b',
        'repo_id': 'Qwen/QwQ-32B',
        'cache_dir': 'Qwen--QwQ-32B',
        'cps': 18,
        'context_length': 8192,
        'vram': 21075.24,
        'function': 'QwQ_32b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Qwen Coder - 32b': {
        'model': 'Qwen Coder - 32b',
        'repo_id': 'Qwen/Qwen2.5-Coder-32B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-Coder-32B-Instruct',
        'cps': 97.47,
        'context_length': 32768,
        'vram': 21120.81,
        'function': 'QwenCoder_32b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Qwen - 32b': {
        'model': 'Qwen - 32b',
        'repo_id': 'Qwen/Qwen2.5-32B-Instruct',
        'cache_dir': 'Qwen--Qwen2.5-32B-Instruct',
        'cps': 101.51,
        'context_length': 8192,
        'vram': 21128.30,
        'function': 'Qwen_32b',
        'precision': 'bfloat16',
        'gated': False,
    },
    'Exaone - 32b': {
        'model': 'Exaone - 32b',
        'repo_id': 'LGAI-EXAONE/EXAONE-3.5-32B-Instruct',
        'cache_dir': 'LGAI-EXAONE--EXAONE-3.5-32B-Instruct',
        'cps': 100.54,
        'context_length': 32768,
        'vram': 21982.30,
        'function': 'Exaone_32b',
        # 'precision': 'float32',
        'gated': False,
    },
    'Deepseek R1 - 32b': {
        'model': 'Deepseek R1 - 32b',
        'repo_id': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
        'cache_dir': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
        'cps': 18,
        'context_length': 8192,
        'vram': 22000,
        'function': 'DeepseekR1_32b',
        'precision': 'bfloat16',
        'gated': False,
    },
}

# overrides default max_length parameter of 8192
MODEL_MAX_TOKENS = {
    'Qwen - 1.5b': 4096,
    'Zephyr - 1.6b': 4096,
    'Granite - 2b': 4096,
    'Qwen Coder - 1.5b': 4096,
    'Zephyr - 3b': 4096,
    'Qwen Coder - 3b': 4096,
}

# overrides max_new_tokens parameter of 1024
MODEL_MAX_NEW_TOKENS = {
    'Qwen - 1.5b': 512,
    'Zephyr - 1.6b': 512,
    'Qwen Coder - 1.5b': 512,
    'Deepseek R1 - 7b': 2048,
    'Deepseek R1 - 14b': 2048,
    'Deepseek R1 - 32b': 2048,
    'QwQ - 32b': 2048,
}

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
        # compiles with triton and search requires cuda
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
    'Llava 1.6 Vicuna - 13b': {
        'precision': 'float16',
        'quant': '4-bit',
        'size': '13b',
        'repo_id': 'llava-hf/llava-v1.6-vicuna-13b-hf',
        'cache_dir': 'llava-hf--llava-v1.6-vicuna-13b-hf',
        'requires_cuda': True,
        'vram': '14.1 GB',
        'loader': 'loader_llava_next'
    }
}

OCR_MODELS = {
    'GOT-OCR2': {
        'precision': 'bfloat16',
        'size': '716m',
        'repo_id': 'ctranslate2-4you/GOT-OCR2_0-Customized',
        'cache_dir': 'ctranslate2-4you--GOT-OCR2_0-Customized',
        'requires_cuda': True,
    },
}

TTS_MODELS = {
    "Kokoro": {
        "model": "Kokoro",
        "repo_id": "ctranslate2-4you/Kokoro-82M-light",
        "save_dir": "ctranslate2-4you--Kokoro-82M-light",
        "cps": 20.5,
        "vram": "2GB",
        "precision": "float32",
        "gated": False,
        "allow_patterns": [
            "voices/**",
            "config.json",
            "istftnet.py",
            "kokoro-v0_19.pth",
            "kokoro.py",
            "models.py",
            "plbert.py"
        ],
    },
    "Bark - Normal": {
        "model": "Bark - Normal", 
        "repo_id": "suno/bark",
        "save_dir": "tts",
        "cps": 18.2,
        "vram": "4GB",
        "precision": "float32",
        "gated": False,
        "allow_patterns": [
            "voices/**",
            "config.json",
            "istftnet.py",
            "kokoro-v0_19.pth",
            # "kokoro.py", # using custom source code
            # "models.py", # using custom source code
            "plbert.py"
        ],
        "ignore_patterns": [
            "demo/**",
            "fp16/**",
            ".gitattributes",
            "kokoro-v0_19.onnx",
            "kokoro.py", # using custom source code
            "models.py", # using custom source code
        ]
    },
    "Bark - Small": {
        "model": "Bark - Small", 
        "repo_id": "suno/bark-small",
        "save_dir": "tts",
        "cps": 18.2,
        "vram": "4GB",
        "precision": "float32",
        "gated": False,
        "allow_patterns": [
            "voices/**",
            "config.json",
            "istftnet.py",
            "kokoro-v0_19.pth",
            # "kokoro.py", # using custom source code
            # "models.py", # using custom source code
            "plbert.py"
        ],
        "ignore_patterns": [
            "demo/**",
            "fp16/**",
            ".gitattributes",
            "kokoro-v0_19.onnx",
            "kokoro.py", # using custom source code
            "models.py", # using custom source code
        ]
    },
    "WhisperSpeech": {
        "model": "WhisperSpeech", 
        "repo_id": "WhisperSpeech/WhisperSpeech",
        "save_dir": "tts",
        "cps": 18.2,
        "vram": "4GB",
        "precision": "fp32",
        "gated": False,
        "allow_patterns": [
            "voices/**",
            "config.json",
            "istftnet.py",
            "kokoro-v0_19.pth",
            # "kokoro.py", # using custom source code
            # "models.py", # using custom source code
            "plbert.py"
        ],
        "ignore_patterns": [
            "demo/**",
            "fp16/**",
            ".gitattributes",
            "kokoro-v0_19.onnx",
            "kokoro.py", # using custom source code
            "models.py", # using custom source code
        ]
    },
    "ChatTTS": {
        "model": "ChatTTS", 
        "repo_id": "2Noise/ChatTTS",
        "save_dir": "tts",
        "cps": 18.2,
        "vram": "4GB",
        "precision": "fp32",
        "gated": False,
        "allow_patterns": [
            "asset/**",
            "config/**",
        ],
        "ignore_patterns": [
            "demo/**",
            "fp16/**",
            ".gitattributes",
            "kokoro-v0_19.onnx",
            "kokoro.py", # using custom source code
            "models.py", # using custom source code
        ]
    },
}

JEEVES_MODELS = {
    "Exaone - 2.4b": {
        "original_repo": "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct",
        "repo": "ctranslate2-4you/EXAONE-3.5-2.4B-Instruct-ct2-int8",
        "folder_name": "ctranslate2-4you--EXAONE-3.5-2.4B-Instruct-Llamafied-ct2-int8",
        "prompt_format": """[|system|]{jeeves_system_message}[|endofturn|]
[|user|]{user_message}
[|endofturn|]
[|assistant|]"""
    },
    "Llama - 3b": {
        "original_repo": "meta-llama/Llama-3.2-3B-Instruct",
        "repo": "ctranslate2-4you/Llama-3.2-3B-Instruct-ct2-int8",
        "folder_name": "ctranslate2-4you--Llama-3.2-3B-Instruct-ct2-int8",
        "prompt_format": """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023

{jeeves_system_message}<|eot_id|>
<|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""
    },
    "Qwen - 3b": {
        "original_repo": "Qwen/Qwen2.5-3B-Instruct",
        "repo": "ctranslate2-4you/Qwen2.5-3B-Instruct-ct2-int8",
        "folder_name": "ctranslate2-4you--Qwen2.5-3B-Instruct-ct2-int8",
        "prompt_format": """<|im_start|>system
{jeeves_system_message}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant"""
    },
    "Danube - 4b": {
        "original_repo": "h2oai/h2o-danube3-4b-chat",
        "repo": "ctranslate2-4you/h2o-danube3-4b-chat-ct2-int8",
        "folder_name": "ctranslate2-4you--h2o-danube3.1-4b-chat-ct2-int8",
        "prompt_format": """<|system|>{jeeves_system_message}</s><|prompt|>{user_message}</s><|answer|>"""
    },
    "Exaone - 7.8b": {
        "original_repo": "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct",
        "repo": "ctranslate2-4you/EXAONE-3.5-7.8B-Instruct-ct2-int8",
        "folder_name": "ctranslate2-4you--EXAONE-3.5-7.8B-Instruct-Llamafied-ct2-int8",
        "prompt_format": """[|system|]{jeeves_system_message}[|endofturn|]
[|user|]{user_message}
[|endofturn|]
[|assistant|]"""
    },
}

WHISPER_SPEECH_MODELS = {
    "s2a": {
        "s2a-q4-tiny": ("s2a-q4-tiny-en+pl.model", 74),
        "s2a-q4-base": ("s2a-q4-base-en+pl.model", 203),
        "s2a-q4-hq-fast": ("s2a-q4-hq-fast-en+pl.model", 380),
        # "s2a-v1.1-small": ("s2a-v1.1-small-en+pl-noyt.model", 437),
        # "s2a-q4-small": ("s2a-q4-small-en+pl.model", 874),
    },
    "t2s": {
        "t2s-tiny": ("t2s-tiny-en+pl.model", 74),
        "t2s-base": ("t2s-base-en+pl.model", 193),
        "t2s-hq-fast": ("t2s-hq-fast-en+pl.model", 743),
        # "t2s-fast-small": ("t2s-fast-small-en+pl.model", 743),
        # "t2s-small": ("t2s-small-en+pl.model", 856),
        # "t2s-v1.1-small": ("t2s-v1.1-small-en+pl.model", 429),
        # "t2s-fast-medium": ("t2s-fast-medium-en+pl+yt.model", 1310)
    }
}

WHISPER_MODELS = {
    # LARGE-V3
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
    # MEDIUM.EN
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
    # SMALL.EN
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
    # BASE.EN
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
    # TINY.EN
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
    # ".pdf": "PyMuPDFLoader",
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

# stuff to include/exclude based on whether "show_thinking" is true or false in config.yaml
THINKING_TAGS = {
    "think": ("<think>", "</think>"),
    "thinking": ("<thinking>", "</thinking>")
    # Add more tag pairs as needed
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
    "CHUNKS_ONLY": "Solely query the vector database and get relevant chunks. Very useful to test the chunk size/overlap settings.",
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

scrape_documentation = {
    "Accelerate 1.3.0": {
        "URL": "https://huggingface.co/docs/accelerate/v1.4.0/en",
        "folder": "accelerate_140",
        "scraper_class": "HuggingfaceScraper"
    },
    "aiohttp 3.9.5": {
        "URL": "https://docs.aiohttp.org/en/v3.11.13/",
        "folder": "aiohttp_31113"
    },
    "Argcomplete": {
        "URL": "https://kislyuk.github.io/argcomplete/",
        "folder": "argcomplete"
    },
    "array_api_compat": {
        "URL": "https://data-apis.org/array-api-compat/",
        "folder": "array_api_compat"
    },
    "AutoAWQ": {
        "URL": "https://casper-hansen.github.io/AutoAWQ/",
        "folder": "autoawq"
    },
    "Beautiful Soup 4": {
        "URL": "https://www.crummy.com/software/BeautifulSoup/bs4/doc/",
        "folder": "beautiful_soup_4"
    },
    "bitsandbytes 0.45.1": {
        "URL": "https://huggingface.co/docs/bitsandbytes/v0.45.2/en/index",
        "folder": "bitsandbytes_0452",
        "scraper_class": "HuggingfaceScraper"
    },
    "Black": {
        "URL": "https://black.readthedocs.io/en/stable/",
        "folder": "Black"
    },
    "chardet": {
        "URL": "https://chardet.readthedocs.io/en/stable/",
        "folder": "chardet"
    },
    "charset-normalizer": {
        "URL": "https://charset-normalizer.readthedocs.io/en/stable/",
        "folder": "charset_normalizer"
    },
    "Click": {
        "URL": "https://click.palletsprojects.com/en/stable/",
        "folder": "click"
    },
    "coloredlogs": {
        "URL": "https://coloredlogs.readthedocs.io/en/latest/",
        "folder": "coloredlogs"
    },
    "CTranslate2": {
        "URL": "https://opennmt.net/CTranslate2/",
        "folder": "ctranslate2"
    },
    "cuda-python 12.6.2": {
        "URL": "https://nvidia.github.io/cuda-python/12.6.2/",
        "folder": "cuda-python_1262"
    },
    "cuda-bindings 12.6.2": {
        "URL": "https://nvidia.github.io/cuda-python/cuda-bindings/12.6.2/",
        "folder": "cuda-bindings_1262"
    },
    "cuda-core 0.1.1": {
        "URL": "https://nvidia.github.io/cuda-python/cuda-core/0.1.1/",
        "folder": "cuda-core_011"
    },
    "cuda-cooperative": {
        "URL": "https://nvidia.github.io/cccl/cuda_cooperative/",
        "folder": "cuda-cooperative"
    },
    "cuda-parallel": {
        "URL": "https://nvidia.github.io/cccl/cuda_parallel/",
        "folder": "cuda_parallel"
    },
    "cuda-nvmath": {
        "URL": "https://docs.nvidia.com/cuda/nvmath-python/0.2.1/",
        "folder": "cuda_nvmath"
    },
    "cuDF": {
        "URL": "https://docs.rapids.ai/api/cudf/stable/",
        "folder": "cuDF"
    },
    "CuPy": {
        "URL": "https://docs.cupy.dev/en/stable/",
        "folder": "cupy"
    },
    "dill": {
        "URL": "https://dill.readthedocs.io/en/latest/",
        "folder": "dill"
    },
    "einops": {
        "URL": "https://einops.rocks/",
        "folder": "einops"
    },
    "einx": {
        "URL": "https://einx.readthedocs.io/en/stable/",
        "folder": "einx",
        "scraper_class": "ReadthedocsScraper"
    },
    "fastcore": {
        "URL": "https://fastcore.fast.ai/",
        "folder": "fastcore",
    },
    "fsspec": {
        "URL": "https://filesystem-spec.readthedocs.io/en/stable/",
        "folder": "fsspec",
        "scraper_class": "ReadthedocsScraper"
    },
    "gTTS": {
        "URL": "https://gtts.readthedocs.io/en/latest/",
        "folder": "gtts"
    },
    "Huggingface Hub 0.28.1": {
        "URL": "https://huggingface.co/docs/huggingface_hub/v0.29.1/en/",
        "folder": "huggingface_hub_0291",
        "scraper_class": "HuggingfaceScraper"
    },
    "humanfriendly": {
        "URL": "https://humanfriendly.readthedocs.io/en/latest/",
        "folder": "humanfriendly"
    },
    "isort": {
        "URL": "https://pycqa.github.io/isort/",
        "folder": "isort"
    },
    "Jinja": {
        "URL": "https://jinja.palletsprojects.com/en/stable/",
        "folder": "jinja"
    },
    "Jiter": {
        "URL": "https://crates.io/crates/jiter",
        "folder": "jiter"
    },
    "jiwer": {
        "URL": "https://jitsi.github.io/jiwer/",
        "folder": "jiwer"
    },
    "joblib": {
        "URL": "https://joblib.readthedocs.io/en/stable/",
        "folder": "joblib"
    },
    "Langchain": {
        "URL": "https://python.langchain.com/api_reference/",
        "folder": "langchain",
        "scraper_class": "LangchainScraper"
    },
    "Librosa": {
        "URL": "https://librosa.org/doc/latest/",
        "folder": "librosa"
    },
    "llama-cpp-python": {
        "URL": "https://llama-cpp-python.readthedocs.io/en/stable/",
        "folder": "llama_cpp_python"
    },
    "llvmlite": {
        "URL": "https://llvmlite.readthedocs.io/en/stable/",
        "folder": "llvmlite",
        "scraper_class": "ReadthedocsScraper"
    },
    "LM Studio": {
        "URL": "https://lmstudio.ai/docs/",
        "folder": "lm_studio"
    },
    "Loguru": {
        "URL": "https://loguru.readthedocs.io/en/stable/",
        "folder": "loguru"
    },
    "lxml 5.3.0": {
        "URL": "https://lxml.de/5.3/",
        "folder": "lxml_530"
    },
    "lxml-html-clean": {
        "URL": "https://lxml-html-clean.readthedocs.io/en/stable/",
        "folder": "lxml_html_clean"
    },
    "marshmallow": {
        "URL": "https://marshmallow.readthedocs.io/en/stable/",
        "folder": "marshmallow"
    },
    # "Matplotlib": {
        # "URL": "https://matplotlib.org/stable/", # won't scrape
        # "folder": "matplotlib"
    # },
    "mpmath": {
        "URL": "https://mpmath.org/doc/current/",
        "folder": "mpmath"
    },
    "msg-parser": {
        "URL": "https://msg-parser.readthedocs.io/en/latest/",
        "folder": "msg_parser"
    },
    "multiprocess": {
        "URL": "https://multiprocess.readthedocs.io/en/stable/",
        "folder": "multiprocess"
    },
    "natsort": {
        "URL": "https://natsort.readthedocs.io/en/stable/",
        "folder": "natsort"
    },
    "NetworkX": {
        "URL": "https://networkx.org/documentation/stable/",
        "folder": "networkx"
    },
    "NLTK": {
        "URL": "https://www.nltk.org/",
        "folder": "nltk"
    },
    # "numba": {
        # "URL": "https://numba.readthedocs.io/",
        # "folder": "numba",
        # "scraper_class": "ReadthedocsScraper"
    # },
    "Numexpr": {
        "URL": "https://numexpr.readthedocs.io/en/latest/",
        "folder": "numexpr"
    },
    "NumPy 1.26": {
        "URL": "https://numpy.org/doc/1.26/",
        "folder": "numpy_126"
    },
    "NumPy (latest stable)": {
        "URL": "https://numpy.org/doc/stable/index.html",
        "folder": "numpy"
    },
    "ONNX": {
        "URL": "https://onnx.ai/onnx/",
        "folder": "onnx"
    },
    "ONNX Runtime": {
        "URL": "https://onnxruntime.ai/docs/api/python/",
        "folder": "onnx_runtime"
    },
    "openai": {
        "URL": "https://platform.openai.com/docs/api-reference/",
        "folder": "openai"
    },
    "openpyxl": {
        "URL": "https://openpyxl.readthedocs.io/en/stable/",
        "folder": "openpyxl"
    },
    "Optimum 1.24.0": {
        "URL": "https://huggingface.co/docs/optimum/v1.24.0/en/",
        "folder": "optimum_1240",
        "scraper_class": "HuggingfaceScraper"
    },
    "packaging": {
        "URL": "https://packaging.pypa.io/en/stable/",
        "folder": "packaging"
    },
    "pandas": {
        "URL": "https://pandas.pydata.org/docs/",
        "folder": "pandas"
    },
    "Pandoc": {
        "URL": "https://pandoc.org",
        "folder": "pandoc"
    },
    "platformdirs": {
        "URL": "https://platformdirs.readthedocs.io/en/stable/",
        "folder": "platformdirs"
    },
    "Playwright": {
        "URL": "https://playwright.dev/python/",
        "folder": "playwright"
    },
    "Pillow": {
        "URL": "https://pillow.readthedocs.io/en/stable/",
        "folder": "pillow"
    },
    # "propcache": {
        # "URL": "https://propcache.aio-libs.org/",
        # "folder": "propcache",
    # },
    "protobuf": {
        "URL": "https://protobuf.dev/",
        "folder": "protobuf"
    },
    "PyAV": {
        "URL": "https://pyav.org/docs/stable/",
        "folder": "pyav"
    },
    "Pydantic": {
        "URL": "https://docs.pydantic.dev/latest/",
        "folder": "pydantic"
    },
    "Pygments": {
        "URL": "https://pygments.org/docs/",
        "folder": "pygments"
    },
    "PyInstaller": {
        "URL": "https://pyinstaller.org/en/stable/",
        "folder": "pyinstaller"
    },
    "PyMuPDF": {
        "URL": "https://pymupdf.readthedocs.io/en/latest/",
        "folder": "pymupdf",
        "scraper_class": "PyMuScraper"
    },
    "PyPDF": {
        "URL": "https://pypdf.readthedocs.io/en/stable/",
        "folder": "pypdf",
        "scraper_class": "ReadthedocsScraper"
    },
    # "Python 3.11": {
        # "URL": "https://docs.python.org/3.11/",
        # "folder": "Python_311",
    # },
    "PyTorch Lightning": {
        "URL": "https://lightning.ai/docs/pytorch/stable/",
        "folder": "pytorch_lightning"
    },
    # "python-docx": {
        # "URL": "https://python-docx.readthedocs.io/en/stable/", # won't scrape
        # "folder": "python_docx"
    # },
    "python-dotenv": {
        "URL": "https://saurabh-kumar.com/python-dotenv/",
        "folder": "python-dotenv"
    },
    "python-oxmsg": {
        "URL": "https://scanny.github.io/python-oxmsg/",
        "folder": "python-oxmsg"
    },
    "PyYAML": {
        "URL": "https://pyyaml.org/wiki/PyYAMLDocumentation",
        "folder": "pyyaml"
    },
    "Pywin32": {
        "URL": "https://mhammond.github.io/pywin32/",
        "folder": "pywin32"
    },
    "Pyside 6": {
        "URL": "https://doc.qt.io/qtforpython-6/",
        "folder": "pyside6",
        "scraper_class": "QtForPythonScraper"
    },
    "RapidFuzz": {
        "URL": "https://rapidfuzz.github.io/RapidFuzz/",
        "folder": "rapidfuzz"
    },
    "Referencing": {
        "URL": "https://referencing.readthedocs.io/en/stable/",
        "folder": "referencing"
    },
    "Requests": {
        "URL": "https://requests.readthedocs.io/en/stable/",
        "folder": "requests"
    },
    "Rich": {
        "URL": "https://rich.readthedocs.io/en/stable/",
        "folder": "rich",
        "scraper_class": "ReadthedocsScraper"
    },
    "rpds-py": {
        "URL": "https://rpds.readthedocs.io/en/stable/",
        "folder": "rpds_py"
    },
    "Rust": {
        "URL": "https://doc.rust-lang.org/stable/",
        "folder": "rust"
    },
    "Rust Docs": {
        "URL": "https://docs.rs",
        "folder": "docs_rs"
    },
    "Rust Std Docs": {
        "URL": "https://doc.rust-lang.org/std/",
        "folder": "rust_std"
    },
    "Rust UV": {
        "URL": "https://docs.astral.sh/uv/",
        "folder": "uv"
    },
    "Safetensors 0.3.2": {
        "URL": "https://huggingface.co/docs/safetensors/v0.3.2/en/",
        "folder": "safetensors_032",
        "scraper_class": "HuggingfaceScraper"
    },
    "scikit-learn": {
        "URL": "https://scikit-learn.org/stable/",
        "folder": "scikit_learn"
    },
    "SciPy 1.15.1": {
        "URL": "https://docs.scipy.org/doc/scipy-1.15.2/",
        "folder": "scipy_1152"
    },
    "Sentence-Transformers": {
        "URL": "https://www.sbert.net/docs",
        "folder": "sentence_transformers"
    },
    "Six": {
        "URL": "https://six.readthedocs.io/",
        "folder": "six",
        "scraper_class": "ReadthedocsScraper"
    },
    "SoundFile 0.11.0": {
        "URL": "https://python-soundfile.readthedocs.io/en/0.13.1/",
        "folder": "soundfile_0131",
        "scraper_class": "ReadthedocsScraper"
    },
    "sounddevice 0.5.1": {
        "URL": "https://python-sounddevice.readthedocs.io/en/0.5.1/",
        "folder": "sounddevice_051"
    },
    "Soupsieve": {
        "URL": "https://facelessuser.github.io/soupsieve/",
        "folder": "soupsieve"
    },
    "Soxr": {
        "URL": "https://python-soxr.readthedocs.io/en/stable/",
        "folder": "soxr"
    },
    "SpaCy": {
        "URL": "https://spacy.io/api",
        "folder": "spacy",
        "scraper_class": "SpacyScraper"
    },
    "SpeechBrain 0.5.15": {
        "URL": "https://speechbrain.readthedocs.io/en/v0.5.15/",
        "folder": "speechbrain_0515",
        "scraper_class": "ReadthedocsScraper"
    },
    "SQLAlchemy 20": {
        "URL": "https://docs.sqlalchemy.org/en/20/",
        "folder": "sqlalchemy_20"
    },
    "sympy": {
        "URL": "https://docs.sympy.org/latest/",
        "folder": "sympy"
    },
    "tenacity": {
        "URL": "https://tenacity.readthedocs.io/en/stable/",
        "folder": "tenacity"
    },
    "Tile DB": {
        "URL": "https://docs.tiledb.com/main",
        "folder": "tiledb",
        "scraper_class": "TileDBScraper"
    },
    "Tile DB Vector Search": {
        "URL": "https://tiledb-inc.github.io/TileDB-Vector-Search/documentation/",
        "folder": "tiledb_vector_search",
        "scraper_class": "TileDBVectorSearchScraper"
    },
    "Timm 1.0.14": {
        "URL": "https://huggingface.co/docs/timm/v1.0.15/en/",
        "folder": "timm_1015",
        "scraper_class": "HuggingfaceScraper"
    },
    "tokenizers": {
        "URL": "https://huggingface.co/docs/tokenizers/v0.20.3/en",
        "folder": "tokenizers_0203",
        "scraper_class": "HuggingfaceScraper"
    },
    "torch 2.6.0": {
        "URL": "https://pytorch.org/docs/2.6/",
        "folder": "torch_26",
        "scraper_class": "PyTorchScraper"
    },
    "Torchaudio 2.6.0": {
        "URL": "https://pytorch.org/audio/2.6.0/",
        "folder": "torchaudio_26",
        "scraper_class": "PyTorchScraper"
    },
    "Torchmetrics": {
        "URL": "https://lightning.ai/docs/torchmetrics/stable/",
        "folder": "torchmetrics"
    },
    "Torchvision 0.21.0": {
        "URL": "https://pytorch.org/vision/0.21/",
        "folder": "torchvision_021",
        "scraper_class": "PyTorchScraper"
    },
    "tqdm": {
        "URL": "https://tqdm.github.io",
        "folder": "tqdm"
    },
    "Transformers 4.49.0": {
        "URL": "https://huggingface.co/docs/transformers/v4.49.0/en",
        "folder": "transformers_4490",
        "scraper_class": "HuggingfaceScraper"
    },
    "Transformers.js 3.0.0": {
        "URL": "https://huggingface.co/docs/transformers.js/v3.0.0/en/",
        "folder": "transformers_js_300",
        "scraper_class": "HuggingfaceScraper"
    },
    "urllib3": {
        "URL": "https://urllib3.readthedocs.io/en/stable/",
        "folder": "urllib3"
    },
    "Unstructured": {
        "URL": "https://docs.unstructured.io/api-reference/api-services/sdk-python",
        "folder": "unstructured"
    },
    "Watchdog": {
        "URL": "https://python-watchdog.readthedocs.io/en/stable/",
        "folder": "watchdog"
    },
    "webdataset": {
        "URL": "https://webdataset.github.io/webdataset/",
        "folder": "webdataset",
        "scraper_class": "ReadthedocsScraper"
    },
    "Wrapt": {
        "URL": "https://wrapt.readthedocs.io/en/master/",
        "folder": "wrapt",
        "scraper_class": "ReadthedocsScraper"
    },
    "xlrd": {
        "URL": "https://xlrd.readthedocs.io/en/stable/",
        "folder": "xlrd",
        "scraper_class": "ReadthedocsScraper"
    },
    "xFormers": {
        "URL": "https://facebookresearch.github.io/xformers/",
        "folder": "xformers"
    },
    "yarl": {
        "URL": "https://yarl.aio-libs.org/en/stable/",
        "folder": "yarl"
    },
}

class CustomButtonStyles:
    # Base colors
    LIGHT_GREY = "#C8C8C8"
    DISABLED_TEXT = "#969696"
    
    # Color definitions with their hover/pressed/disabled variations
    COLORS = {
        "RED": {
            "base": "#320A0A",
            "hover": "#4B0F0F",
            "pressed": "#290909",
            "disabled": "#7D1919"
        },
        "BLUE": {
            "base": "#0A0A32",
            "hover": "#0F0F4B",
            "pressed": "#09092B",
            "disabled": "#19197D"
        },
        "GREEN": {
            "base": "#0A320A",
            "hover": "#0F4B0F",
            "pressed": "#092909",
            "disabled": "#197D19"
        },
        "YELLOW": {
            "base": "#32320A",
            "hover": "#4B4B0F",
            "pressed": "#292909",
            "disabled": "#7D7D19"
        },
        "PURPLE": {
            "base": "#320A32",
            "hover": "#4B0F4B",
            "pressed": "#290929",
            "disabled": "#7D197D"
        },
        "ORANGE": {
            "base": "#321E0A",
            "hover": "#4B2D0F",
            "pressed": "#291909",
            "disabled": "#7D5A19"
        },
        "TEAL": {
            "base": "#0A3232",
            "hover": "#0F4B4B",
            "pressed": "#092929",
            "disabled": "#197D7D"
        },
        "BROWN": {
            "base": "#2B1E0A",
            "hover": "#412D0F",
            "pressed": "#231909",
            "disabled": "#6B5A19"
        }
    }

    @classmethod
    def _generate_button_style(cls, color_values):
        return f"""
            QPushButton {{
                background-color: {color_values['base']};
                color: {cls.LIGHT_GREY};
                padding: 5px;
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {color_values['hover']};
            }}
            QPushButton:pressed {{
                background-color: {color_values['pressed']};
            }}
            QPushButton:disabled {{
                background-color: {color_values['disabled']};
                color: {cls.DISABLED_TEXT};
            }}
        """

for color_name, color_values in CustomButtonStyles.COLORS.items():
    setattr(CustomButtonStyles, f"{color_name}_BUTTON_STYLE", 
            CustomButtonStyles._generate_button_style(color_values))

GPUS_NVIDIA = {
    "GeForce GTX 1630": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 512
    },
    "GeForce GTX 1650 (Apr 2019)": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 896
    },
    "GeForce GTX 1650 (Apr 2020)": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 896
    },
    "GeForce GTX 1650 (Jun 2020)": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 896
    },
    "GeForce GTX 1650 (Laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 1024
    },
    "GeForce GTX 1650 Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 1024
    },
    "GeForce GTX 1650 Ti Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 1024
    },
    "GeForce GTX 1650 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 1024
    },
    "GeForce GTX 1650 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 1280
    },
    "GeForce GTX 1660": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1408
    },
    "GeForce GTX 1660 (Laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1408
    },
    "GeForce GTX 1660 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1408
    },
    "GeForce GTX 1660 Ti Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1536
    },
    "GeForce GTX 1660 Ti (Laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1536
    },
    "GeForce GTX 1660 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1536
    },
    "GeForce RTX 2060": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1920
    },
    "GeForce RTX 2060 Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1920
    },
    "GeForce RTX 2060 (Jan 2019)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1920
    },
    "GeForce RTX 2060 (Jan 2020)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 1920
    },
    "GeForce RTX 3050 Mobile (4GB)": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 2048
    },
    "GeForce RTX 2060 (Dec 2021)": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 2176
    },
    "GeForce RTX 2060 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2176
    },
    "GeForce RTX 2070": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2304
    },
    "GeForce RTX 2070 Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2304
    },
    "GeForce RTX 3050 (GA107-325)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 2304
    },
    "GeForce RTX 3050 (GA106-150)": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2304
    },
    "GeForce RTX 3050 (GA107-150-A1)": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2560
    },
    "GeForce RTX 4050 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 2560
    },
    "GeForce RTX 3050 Ti Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 4,
        "CUDA Cores": 2560
    },
    "GeForce RTX 3050 Mobile (6GB)": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 2560
    },
    "GeForce RTX 2070 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2560
    },
    "GeForce RTX 2070 Super Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 2560
    },
    "GeForce RTX 4060": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 3072
    },
    "GeForce RTX 2080 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 3072
    },
    "GeForce RTX 2080 Super Max-Q": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 3072
    },
    "GeForce RTX 3060": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 3584
    },
    "GeForce RTX 3060 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 6,
        "CUDA Cores": 3840
    },
    "GeForce RTX 4060 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 4352
    },
    "GeForce RTX 2080 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 11,
        "CUDA Cores": 4352
    },
    "GeForce RTX 4070 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 4608
    },
    "GeForce RTX 5070 (laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 4608
    },
    "Nvidia TITAN RTX": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 4608
    },
    "GeForce RTX 3060 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 4864
    },
    "GeForce RTX 3070 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 5120
    },
    "GeForce RTX 3070": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 5888
    },
    "GeForce RTX 4070": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 5888
    },
    "GeForce RTX 5080 Ti (laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 5888
    },
    "GeForce RTX 3070 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 8,
        "CUDA Cores": 6144
    },
    "GeForce RTX 5070": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 6144
    },
    "GeForce RTX 3070 Ti Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": "8-16",
        "CUDA Cores": 6144
    },
    "GeForce RTX 4070 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 7168
    },
    "GeForce RTX 4080 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 7424
    },
    "GeForce RTX 3080 Ti Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 7424
    },
    "GeForce RTX 4070 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 7680
    },
    "GeForce RTX 4080 (AD104-400)": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 7680
    },
    "GeForce RTX 5080 (laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 7680
    },
    "GeForce RTX 4070 Ti Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 8448
    },
    "GeForce RTX 3080": {
        "Brand": "NVIDIA",
        "Size (GB)": 10,
        "CUDA Cores": 8704
    },
    "GeForce RTX 3080 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 12,
        "CUDA Cores": 8960
    },
    "GeForce RTX 5070 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 8960
    },
    "GeForce RTX 4080 (AD103-300)": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 9728
    },
    "GeForce RTX 4090 Mobile/Laptop": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 9728
    },
    "GeForce RTX 4080 Super": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 10240
    },
    "GeForce RTX 3090": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 10496
    },
    "GeForce RTX 5090 (laptop)": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 10496
    },
    "GeForce RTX 3090 Ti": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 10752
    },
    "GeForce RTX 5080": {
        "Brand": "NVIDIA",
        "Size (GB)": 16,
        "CUDA Cores": 10752
    },
    "GeForce RTX 4090 D": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 14592
    },
    "GeForce RTX 4090": {
        "Brand": "NVIDIA",
        "Size (GB)": 24,
        "CUDA Cores": 16384
    },
    "GeForce RTX 5090": {
        "Brand": "NVIDIA",
        "Size (GB)": 32,
        "CUDA Cores": 21760
    }
}

GPUS_AMD = {
    "Radeon RX 7600": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 7600 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 2048
    },
    "Radeon RX 7700 XT": {
        "Brand": "AMD",
        "Size (GB)": 12,
        "Shaders": 3456
    },
    "Radeon RX 7800 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 3840
    },
    "Radeon RX 9070 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 4096
    },
    "Radeon RX 9070": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 3584
    },
    "Radeon RX 7900 GRE": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 5120
    },
    "Radeon RX 7900 XT": {
        "Brand": "AMD",
        "Size (GB)": 20,
        "Shaders": 5376
    },
    "Radeon RX 7900 XTX": {
        "Brand": "AMD",
        "Size (GB)": 24,
        "Shaders": 6144
    },
    "Radeon RX 6300": {
        "Brand": "AMD",
        "Size (GB)": 2,
        "Shaders": 768
    },
    "Radeon RX 6400": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1024
    },
    "Radeon RX 6500 XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1024
    },
    "Radeon RX 6600": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 6600 XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 6650 XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 6700": {
        "Brand": "AMD",
        "Size (GB)": 10,
        "Shaders": 2304
    },
    "Radeon RX 6750 GRE 10GB": {
        "Brand": "AMD",
        "Size (GB)": 10,
        "Shaders": 2560
    },
    "Radeon RX 6750 XT": {
        "Brand": "AMD",
        "Size (GB)": 12,
        "Shaders": 2560
    },
    "Radeon RX 6800": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 3840
    },
    "Radeon RX 6800 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 4608
    },
    "Radeon RX 6900 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 5120
    },
    "Radeon RX 6950 XT": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 5120
    },
    "Radeon RX 5300": {
        "Brand": "AMD",
        "Size (GB)": 3,
        "Shaders": 1408
    },
    "Radeon RX 5300 XT": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1408
    },
    "Radeon RX 5500": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1408
    },
    "Radeon RX 5500 XT": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1408
    },
    "Radeon RX 5600": {
        "Brand": "AMD",
        "Size (GB)": 6,
        "Shaders": 2048
    },
    "Radeon RX 5600 XT": {
        "Brand": "AMD",
        "Size (GB)": 6,
        "Shaders": 2304
    },
    "Radeon RX 5700": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2304
    },
    "Radeon RX 5700 XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2560
    },
    "Radeon RX 5700 XT 50th Anniversary Edition": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2560
    },
    "Radeon RX Vega 56": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 3584
    },
    "Radeon RX Vega 64": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 4096
    },
    "Radeon RX Vega 64 Liquid": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 4096
    },
    "Radeon VII": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 3840
    },
    "Radeon RX 7600S": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 7600M": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 7600M XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 7700S": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 7900M": {
        "Brand": "AMD",
        "Size (GB)": 16,
        "Shaders": 4608
    },
    "Radeon RX 6300M": {
        "Brand": "AMD",
        "Size (GB)": 2,
        "Shaders": 768
    },
    "Radeon RX 6450M": {
        "Brand": "AMD",
        "Size (GB)": 2,
        "Shaders": 768
    },
    "Radeon RX 6550S": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 768
    },
    "Radeon RX 6500M": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1024
    },
    "Radeon RX 6550M": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1024
    },
    "Radeon RX 6600S": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 6700S": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 6600M": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 6650M": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 1792
    },
    "Radeon RX 6800S": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 6650M XT": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2048
    },
    "Radeon RX 6700M": {
        "Brand": "AMD",
        "Size (GB)": 10,
        "Shaders": 2304
    },
    "Radeon RX 6800M": {
        "Brand": "AMD",
        "Size (GB)": 12,
        "Shaders": 2560
    },
    "Radeon RX 6850M XT": {
        "Brand": "AMD",
        "Size (GB)": 12,
        "Shaders": 2560
    },
    "Radeon RX 5300M": {
        "Brand": "AMD",
        "Size (GB)": 3,
        "Shaders": 1408
    },
    "Radeon RX 5500M": {
        "Brand": "AMD",
        "Size (GB)": 4,
        "Shaders": 1408
    },
    "Radeon RX 5600M": {
        "Brand": "AMD",
        "Size (GB)": 6,
        "Shaders": 2304
    },
    "Radeon RX 5700M": {
        "Brand": "AMD",
        "Size (GB)": 8,
        "Shaders": 2304
    }
}

GPUS_INTEL = {
    "Intel Arc A310": {
        "Brand": "Intel",
        "Size (GB)": 4,
        "Shading Cores": 768
    },
    "Intel Arc A380": {
        "Brand": "Intel",
        "Size (GB)": 6,
        "Shading Cores": 1024
    },
    "Intel Arc B570": {
        "Brand": "Intel",
        "Size (GB)": 10,
        "Shading Cores": 2304
    },
    "Intel Arc B580": {
        "Brand": "Intel",
        "Size (GB)": 12,
        "Shading Cores": 2560
    },
    "Intel Arc A580": {
        "Brand": "Intel",
        "Size (GB)": 8,
        "Shading Cores": 3072
    },
    "Intel Arc A750": {
        "Brand": "Intel",
        "Size (GB)": 8,
        "Shading Cores": 3584
    },
    "Intel Arc A770 8GB": {
        "Brand": "Intel",
        "Size (GB)": 8,
        "Shading Cores": 4096
    },
    "Intel Arc A770 16GB": {
        "Brand": "Intel",
        "Size (GB)": 16,
        "Shading Cores": 4096
    }
}

master_questions = [
    "Overview of Program",
    "What is LM Studio and how is it used in this program?",
    "What is Kobold and how is it used in this program?",
    "What is ChatGPT?",
    "What are embedding or vector models?",
    "What are local models and how do I use them?",
    "What local models are available to use?",
    "How do I get a Huggingface access token?",
    "What are context limits for a chat model?",
    "What happens if I exceed the context limit or maximum sequence length and how does the chunk size and overlap setting relate?",
    "How many context should I retrieve when querying the vector database?",
    "What does the chunks only checkbox do?",
    "What are embedding or vector models?",
    "Which embedding or vector model should I choose?",
    "What are the characteristics of vector or embedding models?",
    "What does precision mean regarding embedding models specifically?",
    "What does parameters mean specifically regarding embedding models?",
    "What does dimensions mean specifically regarding embedding models?",
    "What does max sequence mean regarding embedding models?",
    "Tips for using vector or embedding models",
    "What Are Vision Models?",
    "What vision models are available in this program?",
    "Do you have any tips for choosing a vision model?",
    "What is whisper and how does this program use voice recording or transcribing an audio file?",
    "What do the Whisper models do?",
    "How can I record my question for the vector database query?",
    "How can I transcribe an audio file to be put into the vector database?",
    "What is a good batch size to use when transcribing an audio file in this program?",
    "What are the distil variants of the whisper models when transcribing and audio file?",
    "What whisper model should I choose to transcribe a file?",
    "What are floating point formats, precision, and quantization?",
    "What are the common floating point formats?",
    "What does float16 mean?",
    "What is the bfloat16 floating point format?",
    "What is the float16 floating point format?",
    "What does exponent mean in floating point formats?",
    "What are precision and range in floating point formats?",
    "What is the difference between float32, bfloat16 and float16?",
    "What is quantization?",
    "What settings are available in this program and how can I adjust them?",
    "What are the LM Studio Server Settings?",
    "What are the database creation settings and what do they do?",
    "What is the Device setting when creating or querying a vector database?",
    "What is the chunk size setting when creating a vector database?",
    "What is the chunk overlap setting when creating a vector database?",
    "What is the half-precision setting?",
    "What is the contexts setting when querying the vector database?",
    "What is the similarity setting when querying the vector database?",
    "What is the search term filter setting when querying the vector database?",
    "What is the File Type setting when querying the vector database?",
    "What are text to speech models (aka TTS models) and how are they used in this program?",
    "Which text to speech backend or models should I use",
    "Can I back up or restore my vector databases and are they backed up automatically",
    "What happens if I lose a configuration file and can I restore it?",
    "What are some good tips for searching a vector database?",
    "How can I conserve memory or vram usage for this program?",
    "What device is best for querying a vector database?",
    "What are maximum context length of a chat model and and maximum sequence length of an embedding model?",
    "What is the scrape documentation feature in this program?",
    "Which vector or embedding models are available in this program?",
    "What are the Alibaba embedding models?",
    "What are the BGE embedding models?",
    "What are the IBM or granite embedding models?",
    "What are the intfloat embedding models?",
    "What are the NovaSearch or Nova Search embedding models?",
    "What are the sentence transformer or 'sentence-t5' embedding models?",
    "What are the arctic or snowflake embedding models?",
    "What is the sentence transformer static-retrieval embedding model?",
    "What are vision models and which ones does this program offer?",
    "What are the InternVL2.5 vision models?",
    "What are the Florence2 vision models?",
    "What is the Moondream2 vision model?",
    "What is the Mississippi vision model?",
    "What is the Ovis1.6-Llama3.2 vision model?",
    "What is the GLM4v vision model?",
    "What is the Molmo-D-0924 vision model?",
    "What is the Llava 1.6 vision model?",
    "What are chat models and what models does this program offer?",
    "What are the exaone chat models?",
    "What are the qwen 2.5 coder chat models?",
    "What are the qwen chat models and not the coder models?",
    "What is the mistral or mistral small chat model?",
    "What are the IBM or granite chat models?",
    "What is the InternLM chat model?",
    "What is the manage databases Tab?",
    "How can I create a vector database?",
    "What is the Query Database Tab",
    "What is the Tools Tab?",
    "How can I test the various vision models?",
    "What is the Create Database Tab?",
    "What is the manage databases Tab?",
    "What is the Settings Tab?",
    "What is the Models Tab?",
    "What does precision mean?",
    "What is OCR or Optical Character Recognition?",
    "What OCR backends are available in this program?",
    "What is Tesseract?",
    "What is GOT OCR?",
    "How can I use optical character recognition in this program?"
]

jeeves_system_message = "You are a helpful British butler who clearly and directly answers questions in a succinct fashion based on contexts provided to you. If you cannot find the answer within the contexts simply tell me that the contexts do not provide an answer. However, if the contexts partially address a question you answer based on what the contexts say and then briefly summarize the parts of the question that the contexts didn't provide an answer to.  Also, you should be very respectful to the person asking the question and frequently offer traditional butler services like various fancy drinks, snacks, various butler services like shining of shoes, pressing of suites, and stuff like that. Also, if you can't answer the question at all based on the provided contexts, you should apologize profusely and beg to keep your job.  Lastly, it is essential that if there are no contexts actually provided it means that a user's question wasn't relevant and you should state that you can't answer based off of the contexts because there are none.  And it goes without saying you should refuse to answer any questions that are not directly answerable by the provided contexts.  Moreover, some of the contexts might not have relevant information and you should simply ignore them and focus on only answering a user's question.  I cannot emphasize enough that you must gear your answer towards using this program and based your response off of the contexts you receive.  Lastly, in addition to offering to perform stereotypical butler services in the midst of your response, you must always always always end your response with some kind of offering of butler services even they don't want it."
system_message = "You are a helpful person who clearly and directly answers questions in a succinct fashion based on contexts provided to you. If you cannot find the answer within the contexts simply tell me that the contexts do not provide an answer. However, if the contexts partially address my question I still want you to answer based on what the contexts say and then briefly summarize the parts of my question that the contexts didn't provide an answer."
rag_string = "Here are the contexts to base your answer on.  However, I need to reiterate that I only want you to base your response on these contexts and do not use outside knowledge that you may have been trained with."


"""
*********************
Torch Prebuilt Wheels
*********************

# Torch prebuilt wheels are named "cu121," "cu124" or "cu126"
+---------------+----------------------------------
| Wheel Name    | Torch Versions Supported
+---------------+----------------------------------
| cu126         | 2.6.0
| cu124         | 2.6.0, 2.5.1, 2.5.0, 2.4.1, 2.4.0

************
Torch & CUDA
************

# According to https://github.com/pytorch/pytorch/blob/main/.github/scripts/generate_binary_build_matrix.py
# torch prebuilt wheels are compatible with the following Nvidia libraries:
+--------------+------------+------------+------------+
|              |   cu124    |   cu126    |   cu128    | * cu128 not officially released yet
+--------------+------------+------------+------------+
| cuda-nvrtc   | 12.4.127   | 12.6.77    | 12.8.61    |
| cuda-runtime | 12.4.127   | 12.6.77    | 12.8.57    |
| cuda-cupti   | 12.4.127   | 12.6.80    | 12.8.57    |
| cudnn        | 9.1.0.70   | 9.5.1.17   | 9.7.1.26   |
| cublas       | 12.4.5.8   | 12.6.4.1   | 12.8.3.14  |
| cufft        | 11.2.1.3   | 11.3.0.4   | 11.3.3.41  |
| curand       | 10.3.5.147 | 10.3.7.77  | 10.3.9.55  |
| cusolver     | 11.6.1.9   | 11.7.1.2   | 11.7.2.55  |
| cusparse     | 12.3.1.170 | 12.5.4.2   | 12.5.7.53  |
| cusparselt   | 0.6.2      | 0.6.3      | 0.6.3      |
| nccl         | 2.25.1     | 2.25.1     | 2.25.1     |
| nvtx         | 12.4.127   | 12.6.77    | 12.8.55    |
| nvjitlink    | 12.4.127   | 12.6.85    | 12.8.61    |
| cufile       | -          | 1.11.1.6   | 1.13.0.11  |
+--------------+------------+------------+------------+
* cuda-runtime 12.6.77 is from CUDA 12.6.2; otherwise, cu126 uses all CUDA 12.6.3 libraries
* .json files here have all the info: https://developer.download.nvidia.com/compute/cuda/redist/
* in short, torch is not 100% compatible with CUDA 12.1.0 or 12.4.0, for example, or any other version.

************************
"Official Support Matrix
************************ 

# https://github.com/pytorch/pytorch/blob/main/RELEASE.md#release-compatibility-matrix
+-------+----------------------------+----------------------------------------+----------------------------+
| Torch | Python                     | Stable                                 | Experimental               |
+-------+----------------------------+----------------------------------------+----------------------------+
| 2.6   | >=3.9, <=3.13              | CUDA 11.8, 12.4 + CUDNN 9.1.0.70       | CUDA 12.6 + CUDNN 9.5.1.17 | ***
+-------+----------------------------+----------------------------------------+----------------------------+
| 2.5   | >=3.9, <=3.12, (3.13 exp.) | CUDA 11.8, 12.1, 12.4 + CUDNN 9.1.0.70 | None                       |
+-------+----------------------------+----------------------------------------+----------------------------+
| 2.4   | >=3.8, <=3.12              | CUDA 11.8, 12.1 + CUDNN 9.1.0.70       | CUDA 12.4 + CUDNN 9.1.0.70 |
+-------+----------------------------+----------------------------------------+----------------------------+
| 2.3   | >=3.8, <=3.11, (3.12 exp.) | CUDA 11.8 + CUDNN 8.7.0.84             | CUDA 12.1 + CUDNN 8.9.2.26 |
+-------+----------------------------+----------------------------------------+----------------------------+
| 2.2   | >=3.8, <=3.11, (3.12 exp.) | CUDA 11.8 + CUDNN 8.7.0.84             | CUDA 12.1 + CUDNN 8.9.2.26 |
+-------+----------------------------+----------------------------------------+----------------------------+

***********************
Torch & Python & Triton
***********************

# examining the METADATA file for each torch wheel reveals the following compatibility
# torch wheels are named after the torch, cuda, and python version supported - e.g. "2.6.0+cu126-cp312"
+--------+-------+--------+--------+
| Torch  | CUDA  | Python | Triton |
+--------+-------+--------+--------+
| 2.6.0  | cu126 |  3.13  |  3.2.0 |
| 2.6.0  | cu126 |  3.12  |  3.2.0 |
| 2.6.0  | cu126 |  3.11  |  3.2.0 |
| 2.6.0  | cu124 |  3.13  |  3.2.0 |
| 2.6.0  | cu124 |  3.12  |  3.2.0 |
| 2.6.0  | cu124 |  3.11  |  3.2.0 |
| 2.5.1  | cu124 |  3.12  |  3.1.0 |
| 2.5.1  | cu124 |  3.11  |  3.1.0 |
| 2.5.0  | cu124 |  3.12  |  3.1.0 |
| 2.5.0  | cu124 |  3.11  |  3.1.0 |
| 2.4.1  | cu124 |  3.12  |  3.0.0 |
| 2.4.1  | cu124 |  3.11  |  3.0.0 |
| 2.4.0  | cu124 |  3.12  |  3.0.0 |
| 2.4.0  | cu124 |  3.11  |  3.0.0 |
+--------+-------+--------+--------+

*************
Triton Wheels
*************

* 3.0.0 and earlier wheels are located here: https://github.com/jakaline-dev/Triton_win/releases
  * does NOT support Python 3.12

* 3.1.0 and later wheels located here: https://github.com/woct0rdho/triton-windows/releases
 * supports Python 3.12

************
cuDNN & CUDA
************

# According to Nvidia, cuDNN 8.9.2.26 is only compatible up to CUDA 12.2
# For cuDNN 9+, Nvidia promises compatibility for all CUDA 12.x releases, but static linking fluctuates


***********************
LINUX Flash Attention 2
***********************

# Obtained from https://github.com/Dao-AILab/flash-attention/blob/main/.github/workflows/publish.yml
# officially, FA2 only supports up to CUDA 12.4.1, but it seems to work with "cu126"..
+--------------+-----------------------------------------------+-------------------+
| FA2 Version  |                 Torch                         | CUDA (excl. 11.x) |
+--------------+-----------------------------------------------+-------------------+
| v2.7.4.post1 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0             | 12.4.1            |
| v2.7.3       | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.2.post1 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.2       | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.1.post4 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.1.post3 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.1.post2 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241001 | 12.3.2            |
| v2.7.1.post1 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241010 | 12.4.1            |
| v2.7.1       | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0.dev20241010 | 12.4.1            |
| v2.7.0.post2 | 2.2.2, 2.3.1, 2.4.0, 2.5.1                    | 12.4.1            |
| v2.7.0.post1 | 2.2.2, 2.3.1, 2.4.0, 2.5.1                    | 12.4.1            |
| v2.7.0       | 2.2.2, 2.3.1, 2.4.0, 2.5.1                    | 12.3.2            |
| v2.6.3       | 2.2.2, 2.3.1, 2.4.0                           | 12.3.2            |
| v2.6.2       | 2.2.2, 2.3.1, 2.4.0.dev20240527               | 12.3.2            |
| v2.6.1       | 2.2.2, 2.3.1, 2.4.0.dev20240514               | 12.3.2            |
| v2.6.0.post1 | 2.2.2, 2.3.1, 2.4.0.dev20240514               | 12.2.2            |
| v2.6.0       | 2.2.2, 2.3.1, 2.4.0.dev20240512               | 12.2.2            |
| v2.5.9.post1 | 2.2.2, 2.3.0, 2.4.0.dev20240407               | 12.2.2            |
+--------------+-----------------------------------------------+-------------------+

*************************
WINDOWS Flash Attention 2
*************************

# Windows wheels are located here: https://github.com/kingbri1/flash-attention
 # Former name: https://github.com/bdashore3/flash-attention/releases/
# Highly CUDA-specific
+--------------+-----------------------------------+-------------------+
| FA2          |              Torch                | CUDA (excl. 11.x) |
+--------------+-----------------------------------+-------------------+
| v2.7.4.post1 | 2.2.2, 2.3.1, 2.4.0, 2.5.1, 2.6.0 | 12.4.1            |
| v2.7.1.post1 | 2.3.1, 2.4.0, 2.5.1               | 12.4.1            |
| v2.7.0.post2 | 2.3.1, 2.4.0, 2.5.1               | 12.4.1            |
| v2.6.3       | 2.2.2, 2.3.1, 2.4.0               | 12.3.2            |
| v2.6.1       | 2.2.2, 2.3.1                      | 12.3.2            |
| v2.5.9.post2 | 2.2.2, 2.3.1                      | 12.2.2            |
| v2.5.9.post1 | 2.2.2, 2.3.0                      | 12.2.2            |
| v2.5.8       | 2.2.2, 2.3.0                      | 12.2.2            |
| v2.5.6       | 2.1.2, 2.2.2                      | 12.2.2            |
| v2.5.2       | 2.1.2, 2.2.0                      | 12.2.2            |
| v2.4.2       | 2.1.2, 2.2.0                      | 12.2.2            |
+--------------+-----------------------------------+-------------------+

***********************************
Xformers & Flash Attention 2 & CUDA
***********************************

# Highly Torch specific
+------------------+-------+---------------+----------------+---------------+
| Xformers Version | Torch |      FA2      |       CUDA (excl. 11.x)        |
+------------------+-------+---------------+--------------------------------+
| v0.0.29.post3    | 2.6.0 | 2.7.1 - 2.7.2 | 12.1.0, 12.4.1, 12.6.3, 12.8.0 | *pypi
| v0.0.29.post2    | 2.6.0 | 2.7.1 - 2.7.2 | 12.1.0, 12.4.1, 12.6.3, 12.8.0 | *pypi
| v0.0.29.post1    | 2.5.1 | 2.7.1 - 2.7.2 | 12.1.0, 12.4.1                 | *only from pytorch
| v0.0.29 (BUG)    | 2.5.1 |               |                                | *only from pytorch
| v0.0.28.post3    | 2.5.1 |               |                                | *only from pytorch
| v0.0.28.post2    | 2.5.0 |               |                                | *only from pytorch
| v0.0.28.post1    | 2.4.1 |               |                                | *only from pytorch
| v0.0.27.post2    | 2.4.0 |               |                                | *pypi
| v0.0.27.post1    | 2.4.0 |               |                                | *pypi
| v0.0.27          | 2.3.0 |               |                                | *pypi
| v0.0.26.post1    | 2.3.0 |               |                                | *pypi
| v0.0.25.post1    | 2.2.2 |               |                                | *pypi
+------------------+-------+---------------+--------------------------------+
* Torch support determined by https://github.com/facebookresearch/xformers/blob/main/.github/workflows/wheels.yml
* FA2 support determined by by https://github.com/facebookresearch/xformers/blob/main/xformers/ops/fmha/flash.py
* CUDA support determined by https://github.com/facebookresearch/xformers/blob/main/.github/actions/setup-build-cuda/action.yml

***********
Python 3.12
***********

Python 3.12.4 is incompatible with pydantic.v1 as of pydantic==2.7.3
https://github.com/langchain-ai/langchain/issues/22692
***Everything should now be fine as long as Langchain 0.3+ is used, which requires pydantic version 2+***

Other libraries can be checked at: https://pyreadiness.org/3.12/

****************
**One Big Mess**
****************

PER CTRANSLATE2...

Starting from version 4.5.0, ctranslate2 is compatible with cuDNN 9+.

---

According to Ashraf...

either use ct2<4.5 along with torch<2.4 or ct2==4.5 along with torch>=2.4

v4.5.0 works just fine with pip installed cudnn, but if you have a torch version where the cuda binaries are
precompiled such as torch==2.5.0+cu121 or any version that ends with +cu12, this error comes up, the only
solution is downgrade to v4.4.0 at the moment which is strange because it was compiled using cudnn 8.9

+---------------+---------------------+
| Torch Version | Ctranslate2 Version |
+---------------+---------------------+
| 2.*.*+cu121   | <=4.4.0             |
| 2.*.*+cu124   | >=4.5.0             |
| >=2.4.0       | >=4.5.0             |
| <2.4.0        | <4.5.0              |
+---------------+---------------------+
* torch(CUDA or CPU) are compatible with CT2 except for torch +cu121, which requires CT2 <=4.4.0

Update: it's compatible with torch==2.*+cu124 so it's only incompatible with 12.1, I'll open a PR to solve this
  * but his fix didn't work: https://github.com/OpenNMT/CTranslate2/pull/1807

***************
**CTRANSLATE2**
***************

Ctranslate2 3.24.0 - last to use cuDNN 8.1.1 with CUDA 11.2.2 by default
Ctranslate2 4.0.0 - first to use cuDNN 8.8.0 with CUDA 12.2 by default
Ctranslate2 4.5.0 - first to use cuDNN 9.1 with CUDA 12.2 by default

# based on /blob/master/python/tools/prepare_build_environment_windows.sh


"""