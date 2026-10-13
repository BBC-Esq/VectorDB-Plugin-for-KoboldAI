import logging
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import torch
import yaml

from core.constants import PROJECT_ROOT
from core.settings import CONFIG_PATH, read_config, update_config

VECTOR_DB_DIR = PROJECT_ROOT / "Vector_DB"
DOCS_DIR = PROJECT_ROOT / "Docs_for_DB"

PDFS_NEED_OCR_MESSAGE = "PDFs without text content detected."
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff']


def list_databases():
    created = read_config().get("created_databases") or {}
    return {name: (info or {}) for name, info in created.items() if name != "user_manual"}


def database_files(name):
    db_path = VECTOR_DB_DIR / name / "metadata.db"
    if not db_path.exists():
        return None
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name, file_path FROM document_metadata")
        return [(row[0], row[1]) for row in cursor.fetchall()]
    finally:
        conn.close()


def register_database(name, model=None, chunk_size=None, chunk_overlap=None):
    def mutate(config):
        db_settings = config.get("database") or {}
        entries = config.get("created_databases")
        if not isinstance(entries, dict):
            entries = {}
            config["created_databases"] = entries
        entries[name] = {
            "model": model if model is not None else config.get("EMBEDDING_MODEL_NAME"),
            "chunk_size": chunk_size if chunk_size is not None else db_settings.get("chunk_size"),
            "chunk_overlap": chunk_overlap if chunk_overlap is not None else db_settings.get("chunk_overlap"),
        }

    update_config(mutate)


def delete_database(name):
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("Configuration file missing or corrupted.")

    def mutate(config):
        created = config.get("created_databases")
        if isinstance(created, dict):
            created.pop(name, None)
        config.setdefault("database", {})["database_to_search"] = ""

    update_config(mutate)
    dir_path = VECTOR_DB_DIR / name
    if dir_path.exists():
        shutil.rmtree(dir_path, ignore_errors=True)
        if dir_path.exists():
            print(f"Failed to delete: {dir_path}")
            return False
    return True


def find_pdfs_needing_ocr(documents_dir=DOCS_DIR):
    import pymupdf

    pdf_paths = [f for f in Path(documents_dir).iterdir() if f.suffix.lower() == ".pdf"]
    non_ocr_pdfs = []
    for pdf_path in pdf_paths:
        try:
            has_text = False
            with pymupdf.open(str(pdf_path)) as doc:
                for page in doc:
                    if page.get_text().strip():
                        has_text = True
                        break
            if not has_text:
                non_ocr_pdfs.append(pdf_path)
        except Exception as e:
            logging.error(f"Error checking PDF {pdf_path}: {str(e)}")
            continue
    return non_ocr_pdfs


def check_preconditions_for_db_creation(script_dir, database_name, skip_ocr=False):
    if not database_name or len(database_name) < 3 or database_name.lower() in ["null", "none"]:
        return False, "Name must be at least 3 characters long and not be 'null' or 'none.'", []

    vector_db_path = script_dir / "Vector_DB" / database_name
    if vector_db_path.exists():
        return False, (
            f"A vector database called '{database_name}' already exists—"
            "choose a different name or delete the old one first."
        ), []

    config_path = script_dir / 'config.yaml'
    if not config_path.exists():
        return False, "The configuration file (config.yaml) is missing.", []

    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file) or {}

    documents_dir = script_dir / "Docs_for_DB"
    if platform.system() == "Darwin" and any(file.suffix in IMAGE_EXTENSIONS for file in documents_dir.iterdir() if file.is_file()):
        return False, "Image processing has been disabled for MacOS until a fix can be implemented. Please remove all image files and try again.", []

    embedding_model_name = config.get('EMBEDDING_MODEL_NAME')
    if not embedding_model_name:
        return False, "You must first download an embedding model, select it, and choose documents before proceeding.", []

    if not any(file.is_file() for file in documents_dir.iterdir()):
        return False, "No documents are yet added to be processed.", []

    compute_device = config.get('Compute_Device', {}).get('available', [])
    database_creation = config.get('Compute_Device', {}).get('database_creation')
    if ("cuda" in compute_device or "mps" in compute_device) and database_creation == "cpu":
        return False, ("GPU-acceleration is available and strongly recommended. "
                       "Please switch the database creation device to 'cuda' or 'mps', "
                       "or confirm your choice in the GUI."), []

    if not torch.cuda.is_available():
        if config.get('database', {}).get('half', False):
            message = ("CUDA is not available on your system, but half-precision (FP16) "
                       "is selected for database creation. Half-precision requires CUDA. "
                       "Please disable half-precision in the configuration or use a CUDA-enabled GPU.")
            return False, message, []

    if not skip_ocr:
        non_ocr_pdfs = find_pdfs_needing_ocr(documents_dir)
        if non_ocr_pdfs:
            return False, PDFS_NEED_OCR_MESSAGE, non_ocr_pdfs

    return True, "", []


def build_command(database_name):
    return [
        sys.executable, "-c",
        "from db.database_interactions import create_vector_db_in_process; "
        f"create_vector_db_in_process({database_name!r})"
    ]


def start_build(database_name):
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    return subprocess.Popen(
        build_command(database_name),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


def terminate_process_tree(pid):
    import psutil
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    try:
        procs = parent.children(recursive=True)
    except psutil.NoSuchProcess:
        procs = []
    procs.append(parent)
    for p in procs:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
    _, alive = psutil.wait_procs(procs, timeout=5)
    for p in alive:
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass


def remove_partial_database(database_name):
    partial_dir = VECTOR_DB_DIR / database_name
    if partial_dir.exists():
        shutil.rmtree(partial_dir, ignore_errors=True)
