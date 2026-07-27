import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    chunk_size: int = Field(default=700, gt=0, le=100000)
    chunk_overlap: int = Field(default=250, ge=0, le=100000)
    contexts: int = Field(default=5, gt=0, le=1000)
    similarity: float = Field(default=0.7, ge=0.0, le=1.0)
    half: bool = False
    database_to_search: str = ""
    document_types: str = ""
    search_term: str = ""
    pipeline_preset: str = "normal"

    @field_validator("contexts", mode="before")
    @classmethod
    def coerce_contexts(cls, v):
        if isinstance(v, str):
            return int(v)
        return v

    @field_validator("chunk_overlap")
    @classmethod
    def validate_overlap(cls, v: int, info) -> int:
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v

    @field_validator("pipeline_preset")
    @classmethod
    def validate_pipeline_preset(cls, v: str) -> str:
        valid = {"minimal", "low", "normal", "high", "maximum"}
        if v not in valid:
            raise ValueError(f"pipeline_preset must be one of {valid}")
        return v


class ComputeDeviceConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    available: List[str] = Field(default_factory=lambda: ["cpu"])
    database_creation: str = "cpu"
    database_query: str = "cpu"
    gpu_brand: Optional[str] = None

    @field_validator("database_creation", "database_query")
    @classmethod
    def validate_device(cls, v: str, info) -> str:
        if "available" in info.data and v not in info.data["available"]:
            return "cpu"
        return v


class VisionConfig(BaseModel):
    chosen_model: Optional[str] = None


class AppearanceConfig(BaseModel):
    theme: str = "default"


class PlatformInfo(BaseModel):
    os: str = ""


class SupportedQuantizations(BaseModel):
    CPU: List[str] = Field(default_factory=list)
    GPU: List[str] = Field(default_factory=list)


class DatabaseInfo(BaseModel):
    model: str
    chunk_size: int
    chunk_overlap: int


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        extra="allow",
        validate_assignment=True,
    )

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    Compute_Device: ComputeDeviceConfig = Field(default_factory=ComputeDeviceConfig)
    vision: VisionConfig = Field(default_factory=VisionConfig)
    appearance: AppearanceConfig = Field(default_factory=AppearanceConfig)
    Platform_Info: PlatformInfo = Field(default_factory=PlatformInfo)
    Supported_CTranslate2_Quantizations: SupportedQuantizations = Field(
        default_factory=SupportedQuantizations
    )

    EMBEDDING_MODEL_NAME: Optional[str] = None
    EMBEDDING_MODEL_DIMENSIONS: Optional[int] = None
    created_databases: Dict[str, DatabaseInfo] = Field(default_factory=dict)

    _config_path: Path = PrivateAttr(default=Path("config.yaml"))
    _lock: threading.RLock = PrivateAttr(default_factory=threading.RLock)

    @property
    def root_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def docs_dir(self) -> Path:
        return self.root_dir / "Docs_for_DB"

    @property
    def vector_db_dir(self) -> Path:
        return self.root_dir / "Vector_DB"

    @property
    def models_dir(self) -> Path:
        return self.root_dir / "Models"

    @property
    def vector_models_dir(self) -> Path:
        return self.models_dir / "vector"

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "AppConfig":
        config_path = path or Path("config.yaml")
        if not config_path.exists():
            instance = cls()
            instance._config_path = config_path
            instance.save(config_path)
            return instance
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            if "created_databases" in data and isinstance(data["created_databases"], dict):
                for db_name, db_data in data["created_databases"].items():
                    if isinstance(db_data, dict) and not isinstance(db_data, DatabaseInfo):
                        data["created_databases"][db_name] = DatabaseInfo(**db_data)
            instance = cls(**data)
            instance._config_path = config_path
            return instance
        except Exception as e:
            print(f"Error loading config: {e}")
            instance = cls()
            instance._config_path = config_path
            return instance

    def save(self, path: Optional[Path] = None) -> None:
        save_path = path or self._config_path
        with self._lock:
            data = self.model_dump()
            temp_path = save_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True)
            temp_path.replace(save_path)

    def update_field(self, field_path: str, value: Any) -> None:
        with self._lock:
            parts = field_path.split(".")
            obj = self
            for part in parts[:-1]:
                obj = getattr(obj, part)
            setattr(obj, parts[-1], value)
            self.save()

    def update_setting(self, field_path: str, value: Any) -> tuple[bool, str]:
        try:
            self.update_field(field_path, value)
            return True, "Setting updated successfully"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error updating setting: {str(e)}"

    def add_database(self, name: str, model_path: str, chunk_size: int, chunk_overlap: int) -> None:
        self.created_databases[name] = DatabaseInfo(
            model=model_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.save()

    def remove_database(self, name: str) -> None:
        if name in self.created_databases:
            del self.created_databases[name]
            self.save()

    def get_user_databases(self) -> List[str]:
        return list(self.created_databases.keys())


_config_instance: Optional[AppConfig] = None
_config_lock = threading.Lock()


def get_config() -> AppConfig:
    global _config_instance
    if _config_instance is None:
        with _config_lock:
            if _config_instance is None:
                _config_instance = AppConfig.load()
    return _config_instance


def reload_config() -> AppConfig:
    global _config_instance
    with _config_lock:
        _config_instance = AppConfig.load()
    return _config_instance
