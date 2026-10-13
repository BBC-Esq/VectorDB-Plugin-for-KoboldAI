import json
from pathlib import Path

import yaml

from core.constants import PROJECT_ROOT, VISION_MODELS
from core.locks import config_lock
from core.utilities import save_config_atomically

CONFIG_PATH = PROJECT_ROOT / "config.yaml"

PIPELINE_PRESET_NAMES = ("minimal", "low", "normal", "high", "maximum")

SETTINGS = {
    "embedding-model": "Embedding model used to create new databases",
    "vision-model": "Vision model that describes images while a database is created",
    "chunk-size": "Characters in each chunk of a new database",
    "chunk-overlap": "Characters shared by neighboring chunks",
    "create-device": "Device that creates databases: cpu or cuda",
    "search-device": "Device that searches databases: cpu or cuda",
    "half": "Use half precision on the GPU: on or off",
    "contexts": "Most passages a search returns",
    "similarity": "Lowest similarity score (0 to 1) a passage needs to be returned",
    "pipeline": "CPU workers used while creating a database: " + ", ".join(PIPELINE_PRESET_NAMES),
}


def read_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def update_config(mutate):
    with config_lock:
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


def set_hf_token(token):
    token = (token or "").strip()
    if not token:
        raise ValueError("The token is empty.")
    update_config(lambda config: config.__setitem__("hf_access_token", token))


def clear_hf_token():
    update_config(lambda config: config.__setitem__("hf_access_token", None))


def _section(config, name):
    section = config.get(name)
    if not isinstance(section, dict):
        section = {}
        config[name] = section
    return section


def _defaults():
    from core.config import DatabaseConfig

    return DatabaseConfig()


def current_settings(config=None):
    from core.downloads import vector_model_for_path

    config = read_config() if config is None else config
    defaults = _defaults()
    database = config.get("database") if isinstance(config.get("database"), dict) else {}
    compute = config.get("Compute_Device") if isinstance(config.get("Compute_Device"), dict) else {}
    vision = config.get("vision") if isinstance(config.get("vision"), dict) else {}
    model_path = config.get("EMBEDDING_MODEL_NAME")
    model = vector_model_for_path(model_path)
    return {
        "embedding-model": model["name"] if model else (Path(model_path).name if model_path else None),
        "vision-model": vision.get("chosen_model"),
        "chunk-size": database.get("chunk_size", defaults.chunk_size),
        "chunk-overlap": database.get("chunk_overlap", defaults.chunk_overlap),
        "create-device": compute.get("database_creation", "cpu"),
        "search-device": compute.get("database_query", "cpu"),
        "half": "on" if database.get("half", defaults.half) else "off",
        "contexts": database.get("contexts", defaults.contexts),
        "similarity": database.get("similarity", defaults.similarity),
        "pipeline": database.get("pipeline_preset", defaults.pipeline_preset),
    }


def _parse_int(key, value, low, high):
    try:
        number = int(str(value).strip())
    except ValueError:
        raise ValueError(f"{key} must be a whole number.") from None
    if not low <= number <= high:
        raise ValueError(f"{key} must be between {low} and {high}.")
    return number


def _parse_switch(key, value):
    text = str(value).strip().lower()
    if text in ("on", "true", "yes", "1"):
        return True
    if text in ("off", "false", "no", "0"):
        return False
    raise ValueError(f"{key} must be on or off.")


def set_chunking(chunk_size=None, chunk_overlap=None):
    defaults = _defaults()

    def mutate(config):
        database = _section(config, "database")
        size = chunk_size if chunk_size is not None else database.get("chunk_size", defaults.chunk_size)
        overlap = chunk_overlap if chunk_overlap is not None else database.get("chunk_overlap", defaults.chunk_overlap)
        if not 1 <= size <= 100000:
            raise ValueError("chunk-size must be between 1 and 100000.")
        if not 0 <= overlap < size:
            raise ValueError(f"chunk-overlap ({overlap}) must be at least 0 and smaller than chunk-size ({size}).")
        database["chunk_size"] = size
        database["chunk_overlap"] = overlap

    update_config(mutate)


def resolve_vision_model(name):
    wanted = str(name).strip().lower()
    for model_name in VISION_MODELS:
        if wanted == model_name.lower():
            return model_name
    matches = [n for n in VISION_MODELS if wanted and wanted in n.lower()]
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"There is no vision model called '{name}'. Choose one of: {', '.join(VISION_MODELS)}.")


def change_setting(key, value):
    if key not in SETTINGS:
        raise ValueError(f"There is no setting called '{key}'. Settings: {', '.join(SETTINGS)}.")
    if key == "embedding-model":
        from core.downloads import is_vector_model_downloaded, model_directory, resolve_vector_model

        model = resolve_vector_model(value)
        if not is_vector_model_downloaded(model):
            raise ValueError(f"{model['name']} has not been downloaded yet.")
        set_embedding_model(model_directory(model))
        return model["name"]
    if key == "vision-model":
        from core.utilities import runs_on_this_hardware

        name = resolve_vision_model(value)
        if not runs_on_this_hardware(VISION_MODELS[name]):
            raise ValueError(f"{name} needs a supported NVIDIA GPU, which this computer does not have.")
        update_config(lambda config: _section(config, "vision").__setitem__("chosen_model", name))
        return name
    if key in ("chunk-size", "chunk-overlap"):
        number = _parse_int(key, value, 1 if key == "chunk-size" else 0, 100000)
        if key == "chunk-size":
            set_chunking(chunk_size=number)
        else:
            set_chunking(chunk_overlap=number)
        return number
    if key in ("create-device", "search-device"):
        device = str(value).strip().lower()

        def mutate(config):
            compute = _section(config, "Compute_Device")
            available = compute.get("available") or ["cpu"]
            if device not in available:
                raise ValueError(f"{key} must be one of: {', '.join(available)}.")
            compute["database_creation" if key == "create-device" else "database_query"] = device

        update_config(mutate)
        return device
    if key == "half":
        enabled = _parse_switch(key, value)
        update_config(lambda config: _section(config, "database").__setitem__("half", enabled))
        return "on" if enabled else "off"
    if key == "contexts":
        number = _parse_int(key, value, 1, 1000)
        update_config(lambda config: _section(config, "database").__setitem__("contexts", number))
        return number
    if key == "similarity":
        try:
            number = float(str(value).strip())
        except ValueError:
            raise ValueError("similarity must be a number from 0 to 1.") from None
        if not 0.0 <= number <= 1.0:
            raise ValueError("similarity must be a number from 0 to 1.")
        update_config(lambda config: _section(config, "database").__setitem__("similarity", number))
        return number
    preset = str(value).strip().lower()
    if preset not in PIPELINE_PRESET_NAMES:
        raise ValueError(f"pipeline must be one of: {', '.join(PIPELINE_PRESET_NAMES)}.")
    update_config(lambda config: _section(config, "database").__setitem__("pipeline_preset", preset))
    return preset
