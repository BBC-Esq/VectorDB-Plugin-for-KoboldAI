import json
import logging
import os
import platform
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from core.constants import (
    BUILD_COMPLETE_MARKER, DB_FOLDER_CREATED_MARKER, NOT_ADDED_MARKER, PROJECT_ROOT, VECTOR_MODELS, VISION_MODELS,
)
from core.locks import exclusive
from core.settings import CONFIG_PATH, read_config, update_config
from core.utilities import runs_on_this_hardware

VECTOR_DB_DIR = PROJECT_ROOT / "Vector_DB"
DOCS_DIR = PROJECT_ROOT / "Docs_for_DB"

PDFS_NEED_OCR_MESSAGE = "PDFs without text content detected."
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff']

TILEDB_DEEPEST_RELATIVE_PATH = 150
PATH_SAFETY_MARGIN = 10
WINDOWS_MAX_PATH = 259


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


def _needs_ocr_worker(path):
    import fitz
    from core.pdf_ocr_gate import document_needs_ocr
    try:
        with fitz.open(path) as doc:
            return document_needs_ocr(doc)
    except Exception as e:
        logging.error(f"PDF check error {path}: {e}")
        return True


def find_pdfs_needing_ocr(documents_dir=DOCS_DIR):
    import multiprocessing as mp
    try:
        import psutil
        physical = psutil.cpu_count(logical=False) or mp.cpu_count()
    except ImportError:
        logical = mp.cpu_count()
        physical = max(1, max(logical // 2, logical - 4))
    n_threads = max(1, physical - 1)

    try:
        with os.scandir(documents_dir) as it:
            pdf_paths = [Path(entry.path) for entry in it if entry.name.lower().endswith(".pdf")]
    except OSError:
        pdf_paths = []
    if not pdf_paths:
        return []

    with ThreadPoolExecutor(max_workers=n_threads) as ex:
        mask = list(ex.map(_needs_ocr_worker, map(str, pdf_paths)))
    return [p for p, flag in zip(pdf_paths, mask) if flag]


def max_database_name_length(project_root=PROJECT_ROOT):
    base = len(str(Path(project_root) / "Vector_DB")) + 1
    return WINDOWS_MAX_PATH - base - TILEDB_DEEPEST_RELATIVE_PATH - PATH_SAFETY_MARGIN


def database_name_problem(database_name, script_dir=PROJECT_ROOT):
    if not database_name or len(database_name) < 3 or database_name.lower() in ["null", "none"]:
        return "Name must be at least 3 characters long and not be 'null' or 'none.'"

    if not re.fullmatch(r"[a-z0-9_-]+", database_name):
        return "Use only lowercase letters, numbers, hyphens and underscores in the database name."

    name_limit = max_database_name_length(script_dir)
    if len(database_name) > name_limit:
        return ("The database name is too long for the folder this program is installed in, because Windows "
                "limits how long file paths can be. "
                + (f"Use a name of at most {name_limit} characters, or " if name_limit >= 3 else "")
                + "move the program's folder to a shorter path (for example C:\\VectorDB-Plugin-for-KoboldAI).")

    if (Path(script_dir) / "Vector_DB" / database_name).exists():
        return (f"A vector database called '{database_name}' already exists—"
                "choose a different name or delete the old one first.")

    return None


def check_preconditions_for_db_creation(script_dir, database_name, skip_ocr=False):
    if not str(script_dir).isascii():
        return False, ("The program's folder path contains accented or other non-English characters:\n\n"
                       f"{script_dir}\n\nThe vector database library cannot create or open databases in such a "
                       "folder. Move the program's folder to a path that uses only English letters and "
                       "numbers (for example C:\\VectorDB-Plugin-for-KoboldAI) and try again."), []

    name_problem = database_name_problem(database_name, script_dir)
    if name_problem:
        return False, name_problem, []

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

    embedding_info = next((m for models in VECTOR_MODELS.values() for m in models
                           if m.get('cache_dir') == Path(embedding_model_name).name), None)
    if embedding_info and not runs_on_this_hardware(embedding_info):
        return False, (f"The selected embedding model ({embedding_info['name']}) requires a supported NVIDIA GPU. "
                       "Choose a different embedding model."), []

    if not any(file.is_file() for file in documents_dir.iterdir()):
        return False, "No documents are yet added to be processed.", []

    if any(file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS for file in documents_dir.iterdir()):
        vision_model = (config.get('vision') or {}).get('chosen_model')
        vision_info = VISION_MODELS.get(vision_model)
        if vision_info and not runs_on_this_hardware(vision_info):
            alternatives = ", ".join(name for name, info in VISION_MODELS.items() if runs_on_this_hardware(info))
            return False, (f"Your files include images, but the selected vision model ({vision_model}) requires "
                           "a supported NVIDIA GPU, so the images would not be added to the database. "
                           f"Choose a different vision model ({alternatives}) "
                           "or remove the images from the files to add."), []

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


@dataclass
class BuildResult:
    success: bool
    cancelled: bool
    exit_code: int
    message: str
    not_added: list = field(default_factory=list)


def _remove_temp_root(path):
    for _ in range(8):
        shutil.rmtree(path, ignore_errors=True)
        if not os.path.exists(path):
            return
        time.sleep(0.25)


class DatabaseBuild:
    def __init__(self, database_name):
        self.database_name = database_name
        self.process = None
        self.cancelled = False
        self.completed = False
        self.created_folder = False
        self.not_added = []
        self.model = None
        self.chunk_size = None
        self.chunk_overlap = None

    def run(self, on_line=None):
        with exclusive(f"creating the database '{self.database_name}'"):
            return self._run(on_line)

    def _run(self, on_line):
        config = read_config()
        database_settings = config.get("database") if isinstance(config.get("database"), dict) else {}
        self.model = config.get("EMBEDDING_MODEL_NAME")
        self.chunk_size = database_settings.get("chunk_size")
        self.chunk_overlap = database_settings.get("chunk_overlap")
        temp_root = tempfile.mkdtemp(prefix="vectordb_build_")
        exit_code = -1
        try:
            env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8", "TMPDIR": temp_root}
            self.process = subprocess.Popen(
                build_command(self.database_name),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                cwd=str(PROJECT_ROOT),
                env=env,
            )
            if self.cancelled:
                terminate_process_tree(self.process.pid)
            try:
                for line in self.process.stdout:
                    line = line.rstrip("\n")
                    if line.startswith(NOT_ADDED_MARKER):
                        try:
                            self.not_added = json.loads(line[len(NOT_ADDED_MARKER):])
                        except ValueError:
                            pass
                    elif line == DB_FOLDER_CREATED_MARKER:
                        self.created_folder = True
                    elif line == BUILD_COMPLETE_MARKER:
                        self.completed = True
                    elif line.strip() and on_line is not None:
                        on_line(line)
                exit_code = self.process.wait()
            except KeyboardInterrupt:
                self.cancelled = True
                terminate_process_tree(self.process.pid)
                exit_code = self.process.wait()
        finally:
            if self.process is not None and self.process.poll() is None:
                terminate_process_tree(self.process.pid)
            _remove_temp_root(temp_root)
        return self._finish(exit_code)

    def _finish(self, exit_code):
        if exit_code == 0 or self.completed:
            register_database(self.database_name, self.model, self.chunk_size, self.chunk_overlap)
            message = ("The database finished before the cancel took effect, so it was kept."
                       if self.cancelled else "Database created successfully!")
            return BuildResult(True, False, exit_code, message, self.not_added)
        if self.cancelled or self.created_folder:
            remove_partial_database(self.database_name)
        if self.cancelled:
            return BuildResult(False, True, exit_code,
                               "Database creation was cancelled and any partial files were removed.")
        return BuildResult(False, False, exit_code,
                           f"Database build failed (exit code {exit_code}). Check the log for details.")

    def cancel(self):
        self.cancelled = True
        process = self.process
        if process is not None and process.poll() is None:
            terminate_process_tree(process.pid)


def search_database(name, query, contexts=None, similarity=None, contains="", document_type=""):
    from db.database_interactions import QueryVectorDB

    db = QueryVectorDB(name)
    try:
        texts, metadata = db.search(query, k=contexts, score_threshold=similarity,
                                    search_term=contains or "", document_types=document_type or "")
    finally:
        db.close()
    return [
        {
            "file_name": meta.get("file_name"),
            "file_path": meta.get("file_path"),
            "document_type": meta.get("document_type"),
            "score": meta.get("similarity_score"),
            "text": text,
        }
        for text, meta in zip(texts, metadata)
    ]


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
