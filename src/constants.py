VECTOR_MODELS = {
    'BAAI': [
        {
            'name': 'bge-small-en-v1.5',
            'dimensions': 384,
            'max_sequence': 512,
            'size_mb': 134,
            'repo_id': 'BAAI/bge-small-en-v1.5',
            'cache_dir': 'BAAI_bge-small-en-v1.5',
            'type': 'vector'
        },
        {
            'name': 'bge-base-en-v1.5',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 438,
            'repo_id': 'BAAI/bge-base-en-v1.5',
            'cache_dir': 'BAAI-bge-base-en-v1.5',
            'type': 'vector'
        },
        {
            'name': 'bge-large-en-v1.5',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 1340,
            'repo_id': 'BAAI/bge-large-en-v1.5',
            'cache_dir': 'BAAI_bge-large-en-v1.5',
            'type': 'vector'
        },
    ],
    'hkunlp': [
        {
            'name': 'instructor-base',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 439,
            'repo_id': 'hkunlp/instructor-base',
            'cache_dir': 'hkunlp_instructor-base',
            'type': 'vector'
        },
        {
            'name': 'instructor-large',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 1340,
            'repo_id': 'hkunlp/instructor-large',
            'cache_dir': 'hkunlp_instructor-large',
            'type': 'vector'
        },
        {
            'name': 'instructor-xl',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 4960,
            'repo_id': 'hkunlp/instructor-xl',
            'cache_dir': 'hkunlp_instructor-xl',
            'type': 'vector'
        },
    ],
    'sentence-transformers': [
        {
            'name': 'all-MiniLM-L12-v2',
            'dimensions': 384,
            'max_sequence': 256,
            'size_mb': 120,
            'repo_id': 'sentence-transformers/all-MiniLM-L12-v2',
            'cache_dir': 'sentence-transformers_all-MiniLM-L12-v2',
            'type': 'vector'
        },
        {
            'name': 'all-mpnet-base-v2',
            'dimensions': 768,
            'max_sequence': 384,
            'size_mb': 438,
            'repo_id': 'sentence-transformers/all-mpnet-base-v2',
            'cache_dir': 'sentence-transformers_all-mpnet-base-v2',
            'type': 'vector'
        },
    ],
    'thenlper': [
        {
            'name': 'gte-small',
            'dimensions': 384,
            'max_sequence': 512,
            'size_mb': 67,
            'repo_id': 'thenlper/gte-small',
            'cache_dir': 'thenlper_gte-small',
            'type': 'vector'
        },
        {
            'name': 'gte-base',
            'dimensions': 768,
            'max_sequence': 512,
            'size_mb': 219,
            'repo_id': 'thenlper/gte-base',
            'cache_dir': 'thenlper_gte-base',
            'type': 'vector'
        },
        {
            'name': 'gte-large',
            'dimensions': 1024,
            'max_sequence': 512,
            'size_mb': 670,
            'repo_id': 'thenlper/gte-large',
            'cache_dir': 'thenlper_gte-large',
            'type': 'vector'
        },
    ],
}


VISION_MODELS = {
    'Florence-2-base': {
        'precision': 'autoselect',
        'size': '232m',
        'repo_id': 'microsoft/Florence-2-base',
        'cache_dir': 'vision',
        'requires_cuda': False
    },
    'Florence-2-large': {
        'precision': 'autoselect',
        'size': '770m',
        'repo_id': 'microsoft/Florence-2-large',
        'cache_dir': 'vision',
        'requires_cuda': False
    },
    'Moondream2': {
        'precision': 'float16',
        'size': '2b',
        'repo_id': 'vikhyatk/moondream2',
        'cache_dir': 'vision',
        'requires_cuda': True
    }
}

WHISPER_MODELS = {
    # LARGE-V3
    'Distil Whisper large-v3 - float32': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float32',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper large-v3 - bfloat16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-bfloat16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper large-v3 - float16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Whisper large-v3 - float32': {
        'name': 'Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float32',
        'tokens_per_second': 85,
        'optimal_batch_size': 2,
        'avg_vram_usage': '5.5 GB'
    },
    'Whisper large-v3 - bfloat16': {
        'name': 'Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-bfloat16',
        'tokens_per_second': 95,
        'optimal_batch_size': 3,
        'avg_vram_usage': '3.8 GB'
    },
    'Whisper large-v3 - float16': {
        'name': 'Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float16',
        'tokens_per_second': 100,
        'optimal_batch_size': 3,
        'avg_vram_usage': '3.3 GB'
    },
    # MEDIUM.EN
    'Distil Whisper medium.en - float32': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float32',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper medium.en - bfloat16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-bfloat16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper medium.en - float16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Whisper medium.en - float32': {
        'name': 'Whisper medium.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float32',
        'tokens_per_second': 130,
        'optimal_batch_size': 6,
        'avg_vram_usage': '2.5 GB'
    },
    'Whisper medium.en - bfloat16': {
        'name': 'Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-bfloat16',
        'tokens_per_second': 140,
        'optimal_batch_size': 7,
        'avg_vram_usage': '2.0 GB'
    },
    'Whisper medium.en - float16': {
        'name': 'Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float16',
        'tokens_per_second': 145,
        'optimal_batch_size': 7,
        'avg_vram_usage': '1.8 GB'
    },
    # SMALL.EN
    'Distil Whisper small.en - float32': {
        'name': 'Distil Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float32',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper small.en - bfloat16': {
        'name': 'Distil Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-bfloat16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Distil Whisper small.en - float16': {
        'name': 'Distil Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float16',
        'tokens_per_second': 160,
        'optimal_batch_size': 4,
        'avg_vram_usage': '3.0 GB'
    },
    'Whisper small.en - float32': {
        'name': 'Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float32',
        'tokens_per_second': 180,
        'optimal_batch_size': 14,
        'avg_vram_usage': '1.5 GB'
    },
    'Whisper small.en - bfloat16': {
        'name': 'Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-bfloat16',
        'tokens_per_second': 190,
        'optimal_batch_size': 15,
        'avg_vram_usage': '1.2 GB'
    },
    'Whisper small.en - float16': {
        'name': 'Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float16',
        'tokens_per_second': 195,
        'optimal_batch_size': 15,
        'avg_vram_usage': '1.1 GB'
    },
    # BASE.EN
    'Whisper base.en - float32': {
        'name': 'Whisper base.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float32',
        'tokens_per_second': 230,
        'optimal_batch_size': 22,
        'avg_vram_usage': '1.0 GB'
    },
    'Whisper base.en - bfloat16': {
        'name': 'Whisper base.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-bfloat16',
        'tokens_per_second': 240,
        'optimal_batch_size': 23,
        'avg_vram_usage': '0.85 GB'
    },
    'Whisper base.en - float16': {
        'name': 'Whisper base.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float16',
        'tokens_per_second': 245,
        'optimal_batch_size': 23,
        'avg_vram_usage': '0.8 GB'
    },
    # TINY.EN
    'Whisper tiny.en - float32': {
        'name': 'Whisper tiny.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float32',
        'tokens_per_second': 280,
        'optimal_batch_size': 30,
        'avg_vram_usage': '0.7 GB'
    },
    'Whisper tiny.en - bfloat16': {
        'name': 'Whisper tiny.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-bfloat16',
        'tokens_per_second': 290,
        'optimal_batch_size': 31,
        'avg_vram_usage': '0.6 GB'
    },
    'Whisper tiny.en - float16': {
        'name': 'Whisper tiny.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float16',
        'tokens_per_second': 295,
        'optimal_batch_size': 31,
        'avg_vram_usage': '0.55 GB'
    },
}


DOCUMENT_LOADERS = {
    ".pdf": "PyMuPDFLoader",
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
    ".html": "UnstructuredHTMLLoader",
}


CHUNKS_ONLY_TOOLTIP = "Only return relevant chunks without connecting to the LLM. Extremely useful to test the chunk size/overlap settings."

DOWNLOAD_EMBEDDING_MODEL_TOOLTIP = "Remember, wait until downloading is complete!"