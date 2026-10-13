import difflib
import hashlib
import json
import logging
import os
import shutil
import urllib.request
import zipfile
from datetime import datetime, timezone
from http.client import HTTPException

from core.constants import WIKI_CHUNK_SIZE, WIKI_DATABASE, WIKI_DIR, WIKI_FILE, WIKI_MODEL, WIKI_URL, WIKI_ZIP
from core.databases import VECTOR_DB_DIR, DatabaseBuild, register_database
from core.locks import BusyError, exclusive
from core.settings import CONFIG_PATH, chunk_overlap_for, read_config, update_config

DOWNLOAD_TIMEOUT = 60
INFO_NAME = "wiki.json"
WIKI_FOLDER = VECTOR_DB_DIR / WIKI_DATABASE


def download_wiki():
    request = urllib.request.Request(WIKI_URL, headers={"User-Agent": "VectorDB-Plugin-for-KoboldAI"})
    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response:
            text = response.read().decode("utf-8")
    except (OSError, ValueError, HTTPException) as e:
        raise RuntimeError(f"The KoboldCpp wiki could not be downloaded from {WIKI_URL}: {e}") from None
    text = text.replace("\r\n", "\n")
    if not text.strip():
        raise RuntimeError(f"The KoboldCpp wiki downloaded from {WIKI_URL} was empty.")
    return text


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def saved_wiki():
    try:
        return WIKI_FILE.read_text(encoding="utf-8")
    except OSError:
        return None


def wiki_changes(old, new):
    added = removed = 0
    for line in difflib.unified_diff((old or "").splitlines(), new.splitlines(), lineterm="", n=0):
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return added, removed


def wiki_database_exists():
    return (WIKI_FOLDER / "metadata.db").exists()


def installed_wiki_info():
    try:
        info = json.loads((WIKI_FOLDER / INFO_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return info if isinstance(info, dict) and wiki_database_exists() else None


def shipped_wiki_info():
    try:
        with zipfile.ZipFile(WIKI_ZIP) as archive:
            info = json.loads(archive.read(f"{WIKI_DATABASE}/{INFO_NAME}").decode("utf-8"))
    except (OSError, KeyError, ValueError, zipfile.BadZipFile):
        return None
    return info if isinstance(info, dict) else None


def wiki_entry():
    from core.downloads import model_directory, resolve_vector_model

    return {
        "model": str(model_directory(resolve_vector_model(WIKI_MODEL))),
        "chunk_size": WIKI_CHUNK_SIZE,
        "chunk_overlap": chunk_overlap_for(WIKI_CHUNK_SIZE),
    }


def _swap_in(new_folder):
    old = VECTOR_DB_DIR / f"{WIKI_DATABASE}.previous"
    shutil.rmtree(old, ignore_errors=True)
    if WIKI_FOLDER.exists():
        WIKI_FOLDER.rename(old)
    try:
        new_folder.rename(WIKI_FOLDER)
    except OSError:
        if old.exists():
            old.rename(WIKI_FOLDER)
        raise
    shutil.rmtree(old, ignore_errors=True)


def _extract_shipped():
    staging = VECTOR_DB_DIR / f"{WIKI_DATABASE}.extracting"
    shutil.rmtree(staging, ignore_errors=True)
    try:
        with zipfile.ZipFile(WIKI_ZIP) as archive:
            archive.extractall(staging)
        _swap_in(staging / WIKI_DATABASE)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def install_wiki():
    if not CONFIG_PATH.exists():
        return False
    config = read_config()
    if config.get("wiki_removed"):
        return False
    shipped = shipped_wiki_info()
    installed = False
    if shipped is not None and shipped != installed_wiki_info():
        try:
            with exclusive("installing the KoboldCpp wiki database"):
                if shipped != installed_wiki_info():
                    _extract_shipped()
                    installed = True
        except BusyError:
            pass
        except (OSError, zipfile.BadZipFile) as e:
            logging.error("The KoboldCpp wiki database could not be installed from %s: %s", WIKI_ZIP, e)
    if wiki_database_exists():
        entry = wiki_entry()
        if (config.get("created_databases") or {}).get(WIKI_DATABASE) != entry:
            register_database(WIKI_DATABASE, entry["model"], entry["chunk_size"], entry["chunk_overlap"])
    return installed


def _zip_wiki():
    temporary = WIKI_ZIP.with_name(WIKI_ZIP.name + ".tmp")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(WIKI_FOLDER.rglob("*")):
            archive.write(path, f"{WIKI_DATABASE}/{path.relative_to(WIKI_FOLDER).as_posix()}")
    os.replace(temporary, WIKI_ZIP)


def update_wiki(text, on_line=None):
    backup = VECTOR_DB_DIR / f"{WIKI_DATABASE}.previous"
    result = None
    with exclusive("updating the KoboldCpp wiki database"):
        previous = saved_wiki()
        shutil.rmtree(backup, ignore_errors=True)
        if WIKI_FOLDER.exists():
            try:
                WIKI_FOLDER.rename(backup)
            except OSError:
                raise RuntimeError(f"'{WIKI_DATABASE}' is in use, probably by KoboldCpp. "
                                   "Close KoboldCpp and try again.") from None
        try:
            WIKI_DIR.mkdir(parents=True, exist_ok=True)
            WIKI_FILE.write_text(text, encoding="utf-8", newline="\n")
            entry = wiki_entry()
            result = DatabaseBuild(WIKI_DATABASE, chunk_size=entry["chunk_size"], model=entry["model"],
                                   source_dir=WIKI_DIR).run(on_line)
            if result.success:
                info = {
                    "source": WIKI_URL,
                    "sha256": digest(text),
                    "downloaded": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "model": WIKI_MODEL,
                    "chunk_size": entry["chunk_size"],
                    "chunk_overlap": entry["chunk_overlap"],
                }
                (WIKI_FOLDER / INFO_NAME).write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
                _zip_wiki()
        finally:
            if result is not None and result.success:
                shutil.rmtree(backup, ignore_errors=True)
            else:
                shutil.rmtree(WIKI_FOLDER, ignore_errors=True)
                if backup.exists():
                    backup.rename(WIKI_FOLDER)
                if previous is None:
                    WIKI_FILE.unlink(missing_ok=True)
                else:
                    WIKI_FILE.write_text(previous, encoding="utf-8", newline="\n")
    if result.cancelled:
        raise KeyboardInterrupt
    if not result.success:
        raise RuntimeError(result.message)
    update_config(lambda config: config.pop("wiki_removed", None))
    return result
