import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_cpu = os.cpu_count() or 4

PIPELINE_PRESETS = {
    "minimal": {
        "ingest_threads": 1,
        "ingest_processes": 1,
        "split_max_parallel_workers": 1,
        "tokenize_max_parallel_workers": 1,
        "split_worker_batch_size": 5000,
    },
    "low": {
        "ingest_threads": 4,
        "ingest_processes": 2,
        "split_max_parallel_workers": 2,
        "tokenize_max_parallel_workers": 2,
        "split_worker_batch_size": 3000,
    },
    "normal": {
        "ingest_threads": min(max(_cpu - 2, 1), 8),
        "ingest_processes": min(max(_cpu - 2, 1), 4),
        "split_max_parallel_workers": min(max(_cpu - 2, 1), 4),
        "tokenize_max_parallel_workers": min(max(_cpu - 2, 1), 4),
        "split_worker_batch_size": 2000,
    },
    "high": {
        "ingest_threads": min(max(_cpu - 2, 1), 16),
        "ingest_processes": min(max(_cpu - 2, 1), 8),
        "split_max_parallel_workers": min(max(_cpu - 2, 1), 8),
        "tokenize_max_parallel_workers": min(max(_cpu - 2, 1), 8),
        "split_worker_batch_size": 2000,
    },
    "maximum": {
        "ingest_threads": max(_cpu - 2, 1),
        "ingest_processes": max(_cpu - 2, 1),
        "split_max_parallel_workers": 0,
        "tokenize_max_parallel_workers": 0,
        "split_worker_batch_size": 1000,
    },
}

SUPPORTED_EXTENSIONS = (
    ".pdf", ".docx", ".txt", ".eml", ".msg", ".csv",
    ".xls", ".xlsx", ".xlsm", ".rtf", ".md", ".html", ".htm",
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".eml",
    ".msg",
    ".csv",
    ".xls",
    ".xlsx",
    ".xlsm",
    ".rtf",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".html",
    ".htm",
    ".md",
}

NOT_ADDED_MARKER = "VECTORDB_NOT_ADDED "
DB_FOLDER_CREATED_MARKER = "VECTORDB_FOLDER_CREATED"
BUILD_COMPLETE_MARKER = "VECTORDB_BUILD_COMPLETE"

MIN_CUDA_COMPUTE_CAPABILITY = (7, 5)

MIN_NVIDIA_DRIVER_VERSION = 580

THEMES = {
    "default": {
        "bg_window": "#1e1e1e", "bg_surface": "#161b22", "bg_control": "#263238",
        "bg_control_hover": "#2F4F4F", "bg_dialog_button": "#255a7e", "bg_tab": "#255a7e",
        "bg_tab_selected": "#1e2a88", "bg_tab_hover": "#2b3d93", "bg_menu_selected": "#4A148C",
        "bg_splitter": "#1B5E20", "bg_list_hover": "#006064",
        "text_primary": "#d2d2d2", "text_input": "#a8beb5", "text_placeholder": "#d67373",
        "border_focus": "#6c757d", "selection_bg": "#69a9d4", "selection_fg": "black",
    },
    "auburn": {
        "bg_window": "#161b22", "bg_surface": "#3b301b", "bg_control": "#5a423c",
        "bg_control_hover": "#4a3c2b", "bg_dialog_button": "#6c757d", "bg_tab": "#7a645b",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#9a8072", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#6b5343",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#b28a70",
        "border_focus": "#6c757d", "selection_bg": "#8c6a5a", "selection_fg": "white",
    },
    "black": {
        "bg_window": "#0E0D13", "bg_surface": "#0B0A11", "bg_control": "#0B0A11",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#0B0A11",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#2f343f", "bg_menu_selected": "#39424e",
        "bg_splitter": "#0E0D13", "bg_list_hover": "#39424e",
        "text_primary": "#D1D7E2", "text_input": "#D1D7E2", "text_placeholder": "#7BA8D8",
        "border_focus": "#6c757d", "selection_bg": "#555", "selection_fg": "#D1D7E2",
    },
    "bluey": {
        "bg_window": "#1E2A3A", "bg_surface": "#2C3E50", "bg_control": "#34495E",
        "bg_control_hover": "#2C3E50", "bg_dialog_button": "#34495E", "bg_tab": "#34495E",
        "bg_tab_selected": "#2C3E50", "bg_tab_hover": "#4A6377", "bg_menu_selected": "#2C3E50",
        "bg_splitter": "#2C3E50", "bg_list_hover": "#34495E",
        "text_primary": "#ECF0F1", "text_input": "#ECF0F1", "text_placeholder": "#95A5A6",
        "border_focus": "#7F8C8D", "selection_bg": "#4A6377", "selection_fg": "#ECF0F1",
    },
    "bluish": {
        "bg_window": "#161b22", "bg_surface": "#1b2230", "bg_control": "#2d3c47",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#4b5664",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#60687f", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4b5664",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#89a2a2",
        "border_focus": "#6c757d", "selection_bg": "#4f5a77", "selection_fg": "white",
    },
    "colorblind": {
        "bg_window": "#F0F0F0", "bg_surface": "#E0E0E0", "bg_control": "#A0A0A0",
        "bg_control_hover": "#808080", "bg_dialog_button": "#A0A0A0", "bg_tab": "#777777",
        "bg_tab_selected": "#555", "bg_tab_hover": "#666", "bg_menu_selected": "#888",
        "bg_splitter": "#C0C0C0", "bg_list_hover": "#808080",
        "text_primary": "#000000", "text_input": "#000000", "text_placeholder": "#666",
        "border_focus": "#555", "selection_bg": "#555", "selection_fg": "#FFFFFF",
    },
    "dark_blue": {
        "bg_window": "#1a1d29", "bg_surface": "#252836", "bg_control": "#323842",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#4b4b4b",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#666", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4b4b4b",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#969686",
        "border_focus": "#6c757d", "selection_bg": "#555", "selection_fg": "white",
    },
    "dark_grey": {
        "bg_window": "#1a1d21", "bg_surface": "#2a2e32", "bg_control": "#2a2e32",
        "bg_control_hover": "#3a3e42", "bg_dialog_button": "#3498db", "bg_tab": "#2a2e32",
        "bg_tab_selected": "#3498db", "bg_tab_hover": "#3a3e42", "bg_menu_selected": "#3a3e42",
        "bg_splitter": "#2a2e32", "bg_list_hover": "#3a3e42",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#8a8e92",
        "border_focus": "#4a4e52", "selection_bg": "#4a4e52", "selection_fg": "white",
    },
    "dark_yellow": {
        "bg_window": "#161b22", "bg_surface": "#3b382b", "bg_control": "#5a5a5a",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#7a7664",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#9a9280", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#5a5a5a",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#b2a27a",
        "border_focus": "#6c757d", "selection_bg": "#8c7a5a", "selection_fg": "white",
    },
    "green_grey": {
        "bg_window": "#1b2224", "bg_surface": "#09272b", "bg_control": "#424244",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#4b4b4d",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#666669", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e21", "bg_list_hover": "#4b4b4d",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#96989a",
        "border_focus": "#6c757d", "selection_bg": "#555559", "selection_fg": "white",
    },
    "greenish": {
        "bg_window": "#161b22", "bg_surface": "#1b3016", "bg_control": "#3c472d",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#4f604b",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#608060", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4f604b",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#89a280",
        "border_focus": "#6c757d", "selection_bg": "#5a774f", "selection_fg": "white",
    },
    "grey": {
        "bg_window": "#2D2D2D", "bg_surface": "#383838", "bg_control": "#4E4E4E",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#4E4E4E",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#7E7E7E", "bg_menu_selected": "#39424e",
        "bg_splitter": "#2D2D2D", "bg_list_hover": "#4E4E4E",
        "text_primary": "white", "text_input": "#A0A0A0", "text_placeholder": "#7E7E7E",
        "border_focus": "#6c757d", "selection_bg": "#626262", "selection_fg": "white",
    },
    "hyperbolic": {
        "bg_window": "#1B1B1B", "bg_surface": "#006064", "bg_control": "#4A148C",
        "bg_control_hover": "#673AB7", "bg_dialog_button": "#4A148C", "bg_tab": "#311B92",
        "bg_tab_selected": "#4A148C", "bg_tab_hover": "#5E35B1", "bg_menu_selected": "#4A148C",
        "bg_splitter": "#3E2723", "bg_list_hover": "#0097A7",
        "text_primary": "#E0E0E0", "text_input": "white", "text_placeholder": "#9E9E9E",
        "border_focus": "#B39DDB", "selection_bg": "#0288D1", "selection_fg": "white",
    },
    "jewel": {
        "bg_window": "#161b22", "bg_surface": "#301b38", "bg_control": "#423c57",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#605b6e",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#807a8c", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#534153",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a27aa2",
        "border_focus": "#6c757d", "selection_bg": "#775a7a", "selection_fg": "white",
    },
    "matrix": {
        "bg_window": "#000000", "bg_surface": "#001a00", "bg_control": "#001a00",
        "bg_control_hover": "#003300", "bg_dialog_button": "#001a00", "bg_tab": "#001a00",
        "bg_tab_selected": "#00ff00", "bg_tab_hover": "#003300", "bg_menu_selected": "#003300",
        "bg_splitter": "#00ff00", "bg_list_hover": "#003300",
        "text_primary": "#00ff00", "text_input": "#00ff00", "text_placeholder": "#008000",
        "border_focus": "#008000", "selection_bg": "#003300", "selection_fg": "#00ff00",
    },
    "monet": {
        "bg_window": "#161b22", "bg_surface": "#a8beb5", "bg_control": "#8ca6db",
        "bg_control_hover": "#aacbe8", "bg_dialog_button": "#8ca6db", "bg_tab": "#aacbe8",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#cdd3e5", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#39424e",
        "text_primary": "white", "text_input": "#a8beb5", "text_placeholder": "#aacbe8",
        "border_focus": "#6c757d", "selection_bg": "#9dbf9e", "selection_fg": "black",
    },
    "okeefe": {
        "bg_window": "#161b22", "bg_surface": "#3e3033", "bg_control": "#856d88",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#856d88", "bg_tab": "#907880",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#a79f9d", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#856d88",
        "text_primary": "white", "text_input": "#7a6469", "text_placeholder": "#907880",
        "border_focus": "#6c757d", "selection_bg": "#a88c95", "selection_fg": "white",
    },
    "orangish": {
        "bg_window": "#161b22", "bg_surface": "#30261b", "bg_control": "#4a3b2d",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#60594b",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#807562", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4a3b2d",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a28a70",
        "border_focus": "#6c757d", "selection_bg": "#776855", "selection_fg": "white",
    },
    "puke": {
        "bg_window": "#161b22", "bg_surface": "#303a35", "bg_control": "#4a5a4e",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#6e7e71",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#8c9c89", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4a5a4e",
        "text_primary": "white", "text_input": "#59665c", "text_placeholder": "#6e7e71",
        "border_focus": "#6c757d", "selection_bg": "#7a8c7c", "selection_fg": "white",
    },
    "purplish": {
        "bg_window": "#161b22", "bg_surface": "#301b30", "bg_control": "#423c47",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#5b4b5e",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#806080", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4d4154",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a289a2",
        "border_focus": "#6c757d", "selection_bg": "#5a4f5a", "selection_fg": "white",
    },
    "reddish": {
        "bg_window": "#161b22", "bg_surface": "#30161b", "bg_control": "#472d3c",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#604b4f",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#806060", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#543d41",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a28089",
        "border_focus": "#6c757d", "selection_bg": "#774f5a", "selection_fg": "white",
    },
    "steel_ocean": {
        "bg_window": "#1e2126", "bg_surface": "#1b3a47", "bg_control": "#39424e",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#565e66",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#737c85", "bg_menu_selected": "#39424e",
        "bg_splitter": "#202428", "bg_list_hover": "#565e66",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a2a2a3",
        "border_focus": "#6c757d", "selection_bg": "#6c757d", "selection_fg": "white",
    },
    "tron": {
        "bg_window": "#010b19", "bg_surface": "#011627", "bg_control": "#011627",
        "bg_control_hover": "#00ffff", "bg_dialog_button": "#011627", "bg_tab": "#011627",
        "bg_tab_selected": "#00ffff", "bg_tab_hover": "#405c7d", "bg_menu_selected": "#00ffff",
        "bg_splitter": "#00ffff", "bg_list_hover": "#00ffff",
        "text_primary": "#7dfdfe", "text_input": "#7dfdfe", "text_placeholder": "#405c7d",
        "border_focus": "#7dfdfe", "selection_bg": "#00ffff", "selection_fg": "#010b19",
    },
    "yellowish": {
        "bg_window": "#161b22", "bg_surface": "#302f1b", "bg_control": "#4a4739",
        "bg_control_hover": "#2f343f", "bg_dialog_button": "#6c757d", "bg_tab": "#5e5d4b",
        "bg_tab_selected": "#39424e", "bg_tab_hover": "#807f6a", "bg_menu_selected": "#39424e",
        "bg_splitter": "#1e1e1e", "bg_list_hover": "#4a4739",
        "text_primary": "white", "text_input": "white", "text_placeholder": "#a2a27a",
        "border_focus": "#6c757d", "selection_bg": "#75705b", "selection_fg": "white",
    },
}


VECTOR_MODELS = {
    'Microsoft': [
        {
            'name': 'harrier-oss-v1-0.6b',
            'dimensions': 1024,
            'max_sequence': 8192,
            'size_mb': 1190,
            'repo_id': 'microsoft/harrier-oss-v1-0.6b',
            'cache_dir': 'microsoft--harrier-oss-v1-0.6b',
            'type': 'vector',
            'parameters': '596m',
            'precision': 'bfloat16',
            'multilingual_retrieval': 70.75,
            'english_retrieval': 'N/A',
            'rteb_legal': 'N/A',
            'mteb_code': 'N/A',
            'code_information_retrieval': 'N/A',
            'license': 'mit',
        },
    ],
    'infgrad': [
        {
            'name': 'Jasper-Token-Compression-600M',
            'dimensions': 2048,
            'max_sequence': 8192,
            'size_mb': 1215,
            'repo_id': 'infgrad/Jasper-Token-Compression-600M',
            'cache_dir': 'infgrad--Jasper-Token-Compression-600M',
            'type': 'vector',
            'parameters': '607m',
            'precision': 'bfloat16',
            'multilingual_retrieval': 'N/A',
            'english_retrieval': 66.19,
            'rteb_legal': 43.93,
            'mteb_code': 'N/A',
            'code_information_retrieval': 'N/A',
            'license': 'mit',
            'fp16_unsafe': True,
            'custom_code': True,
        },
    ],
    'IEITYuan': [
        {
            'name': 'Yuan-embedding-2.0-en',
            'dimensions': 1024,
            'max_sequence': 8192,
            'size_mb': 1192,
            'repo_id': 'IEITYuan/Yuan-embedding-2.0-en',
            'cache_dir': 'IEITYuan--Yuan-embedding-2.0-en',
            'type': 'vector',
            'parameters': '596m',
            'precision': 'bfloat16',
            'multilingual_retrieval': 'N/A',
            'english_retrieval': 70.69,
            'rteb_legal': 'N/A',
            'mteb_code': 'N/A',
            'code_information_retrieval': 'N/A',
            'license': 'apache-2.0',
        },
    ],
    'geevec-ai': [
        {
            'name': 'geevec-embeddings-1.0-lite',
            'dimensions': 4096,
            'max_sequence': 8192,
            'size_mb': 732,
            'repo_id': 'geevec-ai/geevec-embeddings-1.0-lite',
            'cache_dir': 'geevec-ai--geevec-embeddings-1.0-lite',
            'type': 'vector',
            'parameters': '366m',
            'precision': 'bfloat16',
            'multilingual_retrieval': 70.91,
            'english_retrieval': 62.23,
            'rteb_legal': 'N/A',
            'mteb_code': 'N/A',
            'code_information_retrieval': 'N/A',
            'license': 'apache-2.0',
            'fp16_unsafe': True,
            'custom_code': True,
        },
    ],
}

VISION_MODELS = {
    'Liquid-VL - 480M': {
        'precision': 'bfloat16',
        'quant': 'n/a',
        'size': '480m',
        'repo_id': 'LiquidAI/LFM2-VL-450M',
        'cache_dir': 'LiquidAI--LFM2-VL-450M',
        'requires_cuda': False,
        'vram': '628 MB',
        'avg_length': 1082,
        'characters_per_second': 435.0,
        'loader': 'loader_liquidvl',
        'vision_component': 'SigLIP2 NaFlex base (86M)',
        'chat_component': 'LFM2-350M',
        'license': 'lfm1.0',
    },
    'Liquid-VL - 1.6B': {
        'precision': 'bfloat16',
        'quant': 'n/a',
        'size': '1.6b',
        'repo_id': 'LiquidAI/LFM2-VL-1.6B',
        'cache_dir': 'LiquidAI--LFM2-VL-1.6B',
        'requires_cuda': True,
        'vram': '1.4 GB',
        'avg_length': 936,
        'characters_per_second': 366.2,
        'loader': 'loader_liquidvl',
        'vision_component': 'SigLIP2 NaFlex shape‑optimized (400M)',
        'chat_component': 'LFM2-1.2B',
        'license': 'lfm1.0',
    },
}

WHISPER_MODELS = {
    'Distil Whisper large-v3.5 - float32': {
        'name': 'Distil Whisper large-v3.5',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-distil-large-v3.5-ct2-float32',
    },
    'Distil Whisper large-v3.5 - bfloat16': {
        'name': 'Distil Whisper large-v3.5',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-distil-large-v3.5-ct2-bfloat16',
    },
    'Distil Whisper large-v3.5 - float16': {
        'name': 'Distil Whisper large-v3.5',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-distil-large-v3.5-ct2-float16',
    },
    'Distil Whisper large-v3 - float32': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float32',
    },
    'Distil Whisper large-v3 - bfloat16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-bfloat16',
    },
    'Distil Whisper large-v3 - float16': {
        'name': 'Distil Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-large-v3-ct2-float16',
    },
    'Whisper large-v3 turbo - float32': {
        'name': 'Whisper large-v3 turbo',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-turbo-ct2-float32',
    },
    'Whisper large-v3 turbo - bfloat16': {
        'name': 'Whisper large-v3 turbo',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-turbo-ct2-bfloat16',
    },
    'Whisper large-v3 turbo - float16': {
        'name': 'Whisper large-v3 turbo',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-turbo-ct2-float16',
    },
    'Whisper large-v3 - float32': {
        'name': 'Whisper large-v3',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float32',
    },
    'Whisper large-v3 - bfloat16': {
        'name': 'Whisper large-v3',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-bfloat16',
    },
    'Whisper large-v3 - float16': {
        'name': 'Whisper large-v3',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-large-v3-ct2-float16',
    },
    'Distil Whisper medium.en - float32': {
        'name': 'Distil Whisper medium.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float32',
    },
    'Distil Whisper medium.en - bfloat16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-bfloat16',
    },
    'Distil Whisper medium.en - float16': {
        'name': 'Distil Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-medium.en-ct2-float16',
    },
    'Whisper medium.en - float32': {
        'name': 'Whisper medium.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float32',
    },
    'Whisper medium.en - bfloat16': {
        'name': 'Whisper medium.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-bfloat16',
    },
    'Whisper medium.en - float16': {
        'name': 'Whisper medium.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-medium.en-ct2-float16',
    },
    'Distil Whisper small.en - float32': {
        'name': 'Distil Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float32',
    },
    'Distil Whisper small.en - bfloat16': {
        'name': 'Distil Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-bfloat16',
    },
    'Distil Whisper small.en - float16': {
        'name': 'Distil Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/distil-whisper-small.en-ct2-float16',
    },
    'Whisper small.en - float32': {
        'name': 'Whisper small.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float32',
    },
    'Whisper small.en - bfloat16': {
        'name': 'Whisper small.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-bfloat16',
    },
    'Whisper small.en - float16': {
        'name': 'Whisper small.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-small.en-ct2-float16',
    },
    'Whisper base.en - float32': {
        'name': 'Whisper base.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float32',
    },
    'Whisper base.en - bfloat16': {
        'name': 'Whisper base.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-bfloat16',
    },
    'Whisper base.en - float16': {
        'name': 'Whisper base.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-base.en-ct2-float16',
    },
    'Whisper tiny.en - float32': {
        'name': 'Whisper tiny.en',
        'precision': 'float32',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float32',
    },
    'Whisper tiny.en - bfloat16': {
        'name': 'Whisper tiny.en',
        'precision': 'bfloat16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-bfloat16',
    },
    'Whisper tiny.en - float16': {
        'name': 'Whisper tiny.en',
        'precision': 'float16',
        'repo_id': 'ctranslate2-4you/whisper-tiny.en-ct2-float16',
    },
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
