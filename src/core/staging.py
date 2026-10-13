import os
import time
from dataclasses import dataclass, field
from multiprocessing import Pool, cpu_count
from pathlib import Path

from core.constants import ALLOWED_EXTENSIONS, PROJECT_ROOT
from db.create_symlinks import _create_single_symlink

DOCS_DIR = PROJECT_ROOT / "Docs_for_DB"


@dataclass
class FileSelection:
    top_level: list = field(default_factory=list)
    nested: list = field(default_factory=list)
    unsupported: list = field(default_factory=list)
    missing: list = field(default_factory=list)


def is_supported(path):
    return Path(path).suffix.lower() in ALLOWED_EXTENSIONS


def collect_files(paths):
    selection = FileSelection()
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            try:
                for child in path.iterdir():
                    if child.is_file():
                        if is_supported(child):
                            selection.top_level.append(str(child))
                        else:
                            selection.unsupported.append(str(child))
                for child in path.rglob("*"):
                    if child.is_file() and child.parent != path and is_supported(child):
                        selection.nested.append(str(child))
            except OSError:
                pass
        elif path.is_file():
            if is_supported(path):
                selection.top_level.append(str(path))
            else:
                selection.unsupported.append(str(path))
        else:
            selection.missing.append(str(path))
    return selection


def stage_files(files, target_dir=DOCS_DIR, on_progress=None, should_stop=None):
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    files = list(files)
    total = len(files)
    made = 0
    errors = []
    step = max(1, total // 100) if total else 1
    last_pct = -1
    last_report = time.monotonic()

    def report(done):
        nonlocal last_pct, last_report
        if on_progress is None or (done % step != 0 and done != total):
            return
        pct = int(done * 100 / total) if total else 100
        now = time.monotonic()
        if pct != last_pct and now - last_report > 0.5:
            on_progress(pct)
            last_pct = pct
            last_report = now

    file_args = [(f, str(target_dir)) for f in files]

    if total > 1000:
        processes = min((total // 10000) + 1, cpu_count())
        with Pool(processes=processes) as pool:
            for done, (ok, err) in enumerate(pool.imap_unordered(_create_single_symlink, file_args), 1):
                if should_stop is not None and should_stop():
                    pool.terminate()
                    break
                if ok:
                    made += 1
                if err:
                    errors.append(err)
                report(done)
    else:
        for done, args in enumerate(file_args, 1):
            if should_stop is not None and should_stop():
                break
            ok, err = _create_single_symlink(args)
            if ok:
                made += 1
            if err:
                errors.append(err)
            report(done)

    return made, errors


def staged_files(target_dir=DOCS_DIR):
    try:
        with os.scandir(target_dir) as it:
            return sorted(entry.name for entry in it if not entry.is_dir(follow_symlinks=False))
    except OSError:
        return []


def remove_staged_file(name, target_dir=DOCS_DIR):
    try:
        (Path(target_dir) / name).unlink()
        return True
    except OSError:
        return False


def clear_staged_files(target_dir=DOCS_DIR):
    removed = 0
    for name in staged_files(target_dir):
        if remove_staged_file(name, target_dir):
            removed += 1
    return removed
