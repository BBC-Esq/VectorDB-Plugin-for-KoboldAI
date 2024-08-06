import os
from pathlib import Path
from huggingface_hub import snapshot_download, HfApi
import logging
import threading

logging.getLogger("transformers").setLevel(logging.ERROR)

def download_model_files(repo_id, local_dir):
    try:
        api = HfApi()
        files_list = api.list_repo_files(repo_id)
        
        top_level_files = [f for f in files_list if '/' not in f]
        if not top_level_files:
            raise ValueError("No top-level files found in the repository.")
        snapshot_download(
            repo_id,
            local_dir=local_dir,
            allow_patterns=top_level_files,
            local_dir_use_symlinks=False,
        )
        print(f"Downloaded top-level files from {repo_id} to {local_dir}")
        return True
    except Exception as e:
        print(f"Failed to download model: {e}")
        return False

def download_model(repo_id):
    folder_name = repo_id.replace('/', '_') # CHANGED FROM TWO DASHES
    current_dir = Path(__file__).resolve().parent
    models_dir = current_dir / "Models" / "vector"
    local_dir = models_dir / folder_name

    os.makedirs(local_dir, exist_ok=True)

    thread = threading.Thread(target=download_model_files, args=(repo_id, local_dir))
    thread.start()
    return thread

if __name__ == "__main__":
    test_repo_id = "thenlper/gte-large"
    download_thread = download_model(test_repo_id)
    download_thread.join()