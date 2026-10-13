import atexit
import fnmatch
import os
import shutil
from pathlib import Path

import humanfriendly
import yaml

from core.constants import PROJECT_ROOT, VECTOR_MODELS

MODELS_DIR = PROJECT_ROOT / "Models"
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
INCOMPLETE_MARKER = ".download_incomplete"

MODEL_DIRECTORIES = {
    "vector": "vector",
}


class DownloadError(Exception):
    pass


def is_complete_download(folder):
    folder = Path(folder)
    return folder.is_dir() and not (folder / INCOMPLETE_MARKER).exists()


def get_hf_token():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            token = (data.get("hf_access_token") or "").strip()
            if token:
                return token
        except Exception:
            pass
    return (os.environ.get("HF_TOKEN") or "").strip() or None


def model_repo_id(model_info):
    if isinstance(model_info, dict):
        return model_info.get("repo_id") or model_info.get("url") or model_info.get("name")
    return model_info


def model_directory_name(model_info):
    repo_id = model_repo_id(model_info)
    if isinstance(repo_id, str):
        return repo_id.replace("/", "--")
    return str(repo_id)


def model_directory(model_info, model_type="vector"):
    sub = MODEL_DIRECTORIES.get(model_type, model_type)
    return MODELS_DIR / sub / model_directory_name(model_info)


def vector_models():
    return [dict(model, vendor=vendor) for vendor, models in VECTOR_MODELS.items() for model in models]


def downloaded_vector_model_names():
    vector_dir = MODELS_DIR / "vector"
    if not vector_dir.exists():
        return set()
    return {d.name for d in vector_dir.iterdir() if is_complete_download(d)}


def is_vector_model_downloaded(model_info):
    return model_directory_name(model_info) in downloaded_vector_model_names()


def find_vector_model(name):
    wanted = str(name).strip().lower()
    for model in vector_models():
        if wanted in (model["name"].lower(), model["repo_id"].lower(), model_directory_name(model).lower()):
            return model
    return None


def resolve_vector_model(name):
    model = find_vector_model(name)
    if model is not None:
        return model
    wanted = str(name).strip().lower()
    matches = [m for m in vector_models() if wanted and wanted in m["name"].lower()]
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise ValueError(f"'{name}' matches more than one embedding model: {', '.join(m['name'] for m in matches)}.")
    raise ValueError(f"There is no embedding model called '{name}'. "
                     f"Choose one of: {', '.join(m['name'] for m in vector_models())}.")


def vector_model_for_path(path):
    if not path:
        return None
    folder = Path(str(path)).name
    return next((m for m in vector_models() if model_directory_name(m) == folder), None)


def _score(model, key):
    value = model.get(key)
    return value if isinstance(value, (int, float)) else None


def model_language(model):
    return "multilingual" if _score(model, "multilingual_retrieval") is not None else "English"


def models_by_language():
    english = sorted((m for m in vector_models() if model_language(m) == "English"),
                     key=lambda m: -(_score(m, "english_retrieval") or 0))
    multilingual = sorted((m for m in vector_models() if model_language(m) == "multilingual"),
                          key=lambda m: -(_score(m, "multilingual_retrieval") or 0))
    return english, multilingual


def language_guidance():
    english, multilingual = models_by_language()
    lines = []
    if english:
        described = []
        for m in english:
            scores = [f"English retrieval {_score(m, 'english_retrieval')}"]
            if _score(m, "rteb_legal") is not None:
                scores.append(f"legal retrieval {_score(m, 'rteb_legal')}")
            described.append(f"{m['name']} ({', '.join(scores)})")
        lines.append("English documents: " + " or ".join(described) + ".")
    if multilingual:
        lines.append("Other languages or a mix of languages: " + " or ".join(
            f"{m['name']} (multilingual retrieval {_score(m, 'multilingual_retrieval')})" for m in multilingual) + ".")
    return lines


class ModelDownloader:
    def __init__(self, model_info, model_type="vector"):
        from huggingface_hub import HfApi
        from huggingface_hub.utils import disable_progress_bars

        self.model_info = model_info
        self.model_type = model_type
        self.hf_token = get_hf_token()
        self.api = HfApi(token=False)
        self.api.timeout = 60
        disable_progress_bars()
        self.local_dir = model_directory(model_info, model_type)

    def cleanup_incomplete_download(self):
        try:
            local_dir = getattr(self, "local_dir", None)
            if not local_dir or not local_dir.exists() or getattr(self, "_had_existing_download", False):
                return
            if not (local_dir / INCOMPLETE_MARKER).exists():
                return
            for child in local_dir.iterdir():
                if child.name == INCOMPLETE_MARKER:
                    continue
                if child.is_dir():
                    shutil.rmtree(child, ignore_errors=True)
                else:
                    child.unlink(missing_ok=True)
            if not any(child.name != INCOMPLETE_MARKER for child in local_dir.iterdir()):
                shutil.rmtree(local_dir, ignore_errors=True)
        except Exception:
            pass

    def get_model_directory_name(self):
        return model_directory_name(self.model_info)

    def get_model_directory(self):
        return model_directory(self.model_info, self.model_type)

    def get_model_url(self):
        return model_repo_id(self.model_info)

    def check_repo_type(self, repo_id):
        from huggingface_hub import HfApi
        from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError

        try:
            repo_info = self.api.repo_info(repo_id, timeout=60, token=False)
            if getattr(repo_info, "private", False):
                return "private"
            if getattr(repo_info, "gated", False):
                return "gated"
            return "public"
        except RepositoryNotFoundError:
            return "not_found"
        except GatedRepoError:
            return "gated"
        except Exception as e:
            msg = str(e).lower()
            if "401" in msg or "403" in msg or "gated" in msg:
                try:
                    api_with_token = HfApi(token=self.hf_token or False)
                    _ = api_with_token.repo_info(repo_id, timeout=60)
                    return "public"
                except GatedRepoError:
                    return "gated"
                except Exception:
                    return "gated" if not self.hf_token else "error"
            return "error"

    def _list_repo_files(self, repo_id, use_token):
        from huggingface_hub import HfApi

        api = self.api if not use_token else HfApi(token=self.hf_token)
        return list(api.list_repo_tree(repo_id, recursive=True))

    def _select_patterns(self, repo_files, allow_patterns, ignore_patterns):
        from huggingface_hub.hf_api import RepoFile

        final_ignore = [
            "*.ckpt",
            "*.onnx",
            "*.h5",
            "*.tflite",
            "*.pb",
            "*.msgpack",
            "*.flax",
            "*.npz",
            "*.tar",
            "*.tar.gz",
            "*.zip",
            "*.rar",
            "*.7z",
            "*.gz",
            "*.bz2",
            "*.xz",
            "*.md",
            "README*",
            "LICENSE*",
            ".*",
            ".gitattributes",
            ".git*",
        ]
        if ignore_patterns:
            final_ignore.extend(ignore_patterns)
        safetensors_files = [f.rfilename for f in repo_files if isinstance(f, RepoFile) and f.rfilename.endswith(".safetensors")]
        bin_files = [f.rfilename for f in repo_files if isinstance(f, RepoFile) and f.rfilename.endswith(".bin")]
        if safetensors_files and bin_files:
            final_ignore.append("*.bin")
            final_ignore.append("*.bin.index.json")
        if safetensors_files or bin_files:
            final_ignore.append("*consolidated*")
        if allow_patterns is None:
            allow_patterns = ["*.json", "*.safetensors", "*.bin", "*.model", "tokenizer*", "vocab*", "merges.txt", "config.yaml", "modules.json", "1_Pooling/*", "sentencepiece.*", "spiece.*"]
            if isinstance(self.model_info, dict) and self.model_info.get("custom_code"):
                allow_patterns.append("*.py")
        return allow_patterns, final_ignore

    def _filter_and_size(self, repo_files, allow_patterns, ignore_patterns):
        from huggingface_hub.hf_api import RepoFile

        included_files = []
        ignored_files = []
        total_size = 0
        for file in repo_files:
            if not isinstance(file, RepoFile):
                continue
            path = file.rfilename
            if any(fnmatch.fnmatch(path, pat) for pat in ignore_patterns):
                ignored_files.append(path)
                continue
            if allow_patterns and not any(fnmatch.fnmatch(path, pat) for pat in allow_patterns):
                ignored_files.append(path)
                continue
            included_files.append(path)
            try:
                if file.size is not None:
                    total_size += int(file.size)
            except Exception:
                pass
        return included_files, ignored_files, total_size

    def _fail(self, msg):
        print(msg)
        raise DownloadError(msg)

    def download(self, allow_patterns=None, ignore_patterns=None):
        from huggingface_hub import snapshot_download

        repo_id = self.get_model_url()
        repo_type = self.check_repo_type(repo_id)
        if repo_type not in ["public", "gated"]:
            if repo_type == "private":
                msg = f"Repository {repo_id} is private and requires a token."
                if not self.hf_token:
                    msg += "\n\nNo Hugging Face access token is set. Set one with 'python cli.py token set' or the File menu."
                self._fail(msg)
            if repo_type == "not_found":
                self._fail(f"Repository {repo_id} not found.")
            self._fail(f"Error checking repository {repo_id}.")
        if repo_type == "gated" and not self.hf_token:
            self._fail(
                f"Repository {repo_id} is gated and requires access and a token.\n\n"
                f"Visit https://huggingface.co/{repo_id} to request access, then set your "
                f"Hugging Face token with 'python cli.py token set' or the File menu."
            )
        local_dir = self.get_model_directory()
        marker = local_dir / INCOMPLETE_MARKER
        had_existing_download = local_dir.exists() and any(local_dir.iterdir()) and not marker.exists()
        self._had_existing_download = had_existing_download
        local_dir.mkdir(parents=True, exist_ok=True)
        marker.touch()
        atexit.register(self.cleanup_incomplete_download)
        try:
            repo_files = self._list_repo_files(repo_id, use_token=(repo_type == "gated"))
            allow_patterns, final_ignore_patterns = self._select_patterns(repo_files, allow_patterns, ignore_patterns)
            included_files, ignored_files, total_size = self._filter_and_size(repo_files, allow_patterns, final_ignore_patterns)
            readable_total_size = humanfriendly.format_size(total_size, binary=True)
            print(f"\nTotal size to be downloaded: {readable_total_size}")
            print("\nFiles to be downloaded:")
            for f in included_files:
                print(f"- {f}")
            print(f"\nDownloading to {local_dir}...")
            download_kwargs = {
                "repo_id": repo_id,
                "local_dir": str(local_dir),
                "max_workers": 8,
                "ignore_patterns": final_ignore_patterns,
                "allow_patterns": allow_patterns,
                "etag_timeout": 60
            }
            if repo_type == "gated" and self.hf_token:
                download_kwargs["token"] = self.hf_token
            else:
                download_kwargs["token"] = False
            snapshot_download(**download_kwargs)
            marker.unlink(missing_ok=True)
            print("\033[92mModel downloaded and ready to use.\033[0m")
            atexit.unregister(self.cleanup_incomplete_download)
            return self.get_model_directory_name()
        except Exception as e:
            msg = f"An error occurred during download: {str(e)}"
            print(msg)
            if not had_existing_download and local_dir.exists():
                try:
                    shutil.rmtree(local_dir)
                except OSError:
                    pass
            raise DownloadError(msg) from e
