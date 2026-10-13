import json
from pathlib import Path

import yaml

from core.constants import PROJECT_ROOT
from core.utilities import save_config_atomically

CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def read_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def update_config(mutate):
    config = read_config()
    mutate(config)
    save_config_atomically(config, CONFIG_PATH, allow_unicode=True)
    return config


def embedding_model_dimensions(model_path):
    name = str(model_path).lower()
    if "stella" in name or "static-retrieval" in name:
        return 1024
    config_json_path = Path(model_path) / "config.json"
    if config_json_path.exists():
        with open(config_json_path, "r", encoding="utf-8") as f:
            model_config = json.load(f)
        dimensions = model_config.get("hidden_size") or model_config.get("d_model")
        if dimensions and isinstance(dimensions, int):
            return dimensions
    return None


def set_embedding_model(model_path):
    def mutate(config):
        if model_path:
            config["EMBEDDING_MODEL_NAME"] = str(model_path)
            dimensions = embedding_model_dimensions(model_path)
            if dimensions:
                config["EMBEDDING_MODEL_DIMENSIONS"] = dimensions
        else:
            config.pop("EMBEDDING_MODEL_NAME", None)
            config.pop("EMBEDDING_MODEL_DIMENSIONS", None)

    return update_config(mutate)
