import platform
import shutil
from pathlib import Path
import logging

import torch
import ctranslate2

from core.constants import PROJECT_ROOT

def get_compute_device_info():
    available_devices = ["cpu"]
    gpu_brand = None

    if torch.cuda.is_available():
        available_devices.append('cuda')
        gpu_brand = "AMD" if torch.version.hip else "NVIDIA" if torch.version.cuda else None

    return {'available': available_devices, 'gpu_brand': gpu_brand}

def get_platform_info():
    return {'os': platform.system().lower()}

def get_supported_quantizations(device_type):
    types = ctranslate2.get_supported_compute_types(device_type)
    filtered_types = [q for q in types if q != 'int16']

    desired_order = ['float32', 'float16', 'bfloat16', 'int8_float32', 'int8_float16', 'int8_bfloat16', 'int8']
    return [q for q in desired_order if q in filtered_types]

def update_config_file(**system_info):
    from core.locks import config_lock
    from core.settings import CONFIG_PATH, update_config

    quantizations = {
        'CPU': get_supported_quantizations('cpu'),
        'GPU': get_supported_quantizations('cuda') if torch.cuda.is_available() else []
    }

    def mutate(config_data):
        compute = config_data.get('Compute_Device')
        if not isinstance(compute, dict):
            compute = {}
            config_data['Compute_Device'] = compute
        compute_device_info = system_info.get('Compute_Device', {})
        compute['available'] = compute_device_info.get('available', ['cpu'])
        compute['gpu_brand'] = compute_device_info.get('gpu_brand', '')

        valid_devices = ['cpu', 'cuda', 'mps']
        for key in ['database_creation', 'database_query']:
            compute[key] = compute.get(key, 'cpu') if compute.get(key) in valid_devices else 'cpu'

        config_data['Supported_CTranslate2_Quantizations'] = quantizations

        for key, value in system_info.items():
            if key not in ('Compute_Device', 'Supported_CTranslate2_Quantizations'):
                config_data[key] = value

    with config_lock:
        if not CONFIG_PATH.exists():
            from core.config import AppConfig
            AppConfig().save(CONFIG_PATH)
        update_config(mutate)

def check_for_necessary_folders():
    folders = [
        "Docs_for_DB",
        "Vector_DB",
        "Models",
        "Models/vector",
        "Models/vision",
        "Models/whisper",
    ]

    for folder in folders:
        (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)

def prepare():
    from core.settings import CONFIG_PATH, update_config

    first_run = not CONFIG_PATH.exists()
    compute_device_info = get_compute_device_info()
    update_config_file(Compute_Device=compute_device_info, Platform_Info=get_platform_info())
    if first_run and 'cuda' in compute_device_info['available']:
        def prefer_gpu(config_data):
            config_data['Compute_Device']['database_creation'] = 'cuda'
            config_data['Compute_Device']['database_query'] = 'cuda'
        update_config(prefer_gpu)
    check_for_necessary_folders()
    from core.wiki import install_wiki
    install_wiki()

def clear_pickle_folder():
    pickle_folder = Path('pickle')
    if pickle_folder.exists():
        shutil.rmtree(pickle_folder, ignore_errors=True)

def delete_chat_history():
    chat_history_path = Path(__file__).resolve().parent.parent / 'chat_history.txt'
    chat_history_path.unlink(missing_ok=True)

def main():
    compute_device_info = get_compute_device_info()
    platform_info = get_platform_info()
    update_config_file(Compute_Device=compute_device_info, Platform_Info=platform_info)
    check_for_necessary_folders()
    delete_chat_history()
    clear_pickle_folder()

if __name__ == "__main__":
    main()
