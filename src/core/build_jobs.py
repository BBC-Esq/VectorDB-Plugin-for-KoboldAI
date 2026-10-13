import json
import logging
import os
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path

from core.constants import PROJECT_ROOT

JOBS_DIR = PROJECT_ROOT / "jobs"
ACTIVE_STATES = ("queued", "downloading", "adding", "ocr", "building")
STARTUP_GRACE_SECONDS = 120
SHOWN_NOT_ADDED = 10


def status_path(name):
    return JOBS_DIR / f"{name}.json"


def log_path(name):
    return JOBS_DIR / f"{name}.log"


def cancel_path(name):
    return JOBS_DIR / f"{name}.cancel"


def read_status(name):
    try:
        data = json.loads(status_path(name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def write_status(status):
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    path = status_path(status["name"])
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def all_statuses():
    statuses = [read_status(path.stem) for path in JOBS_DIR.glob("*.json")] if JOBS_DIR.exists() else []
    return sorted((s for s in statuses if s), key=lambda s: s.get("started") or 0, reverse=True)


def format_duration(seconds):
    seconds = max(0, seconds)
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    minutes, seconds = divmod(int(round(seconds)), 60)
    if minutes < 60:
        return f"{minutes} min {seconds} s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} h {minutes} min"


def _process_started(pid):
    import psutil

    try:
        return psutil.Process(pid).create_time()
    except (psutil.Error, TypeError, ValueError):
        return None


def job_is_running(status):
    if status.get("state") not in ACTIVE_STATES:
        return False
    if status.get("pid") is None:
        return time.time() - (status.get("started") or 0) < STARTUP_GRACE_SECONDS
    started = _process_started(status["pid"])
    return started is not None and abs(started - (status.get("process_started") or started)) < 1


def running_job():
    return next((s for s in all_statuses() if job_is_running(s)), None)


def plan_build(name, paths, embedding_model=None, clear_waiting_files=False):
    from core.databases import database_name_problem, list_databases
    from core.downloads import is_vector_model_downloaded, language_guidance, resolve_vector_model, vector_model_for_path
    from core.locks import busy_message, current_operation
    from core.settings import read_config
    from core.staging import collect_files, staged_files

    name = (name or "").strip()
    problem = database_name_problem(name)
    if problem:
        raise ValueError(problem)
    if name in list_databases():
        raise ValueError(f"A database called '{name}' already exists. Choose another name.")
    running = running_job()
    if running is not None:
        raise ValueError(f"'{running['name']}' is still being created. Start another database when it finishes.")
    holder = current_operation()
    if holder is not None:
        raise ValueError(busy_message(holder))
    if isinstance(paths, str):
        paths = [p for p in paths.replace(";", "\n").splitlines()]
    paths = [str(p).strip().strip('"') for p in (paths or []) if str(p).strip()]
    if not paths:
        raise ValueError("Give at least one full path to a file or folder.")
    resolved = []
    for raw in paths:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            raise ValueError(f"'{raw}' is not a full path. Use full paths such as C:\\Users\\Name\\Documents.")
        if not path.exists():
            raise ValueError(f"'{raw}' does not exist.")
        resolved.append(path)
    selection = collect_files(resolved)
    files = selection.top_level + selection.nested
    if not files:
        skipped = f" {len(selection.unsupported)} file(s) of other types were found." if selection.unsupported else ""
        raise ValueError("None of these paths contain files this program can read (PDF, Word, text, Markdown, HTML, "
                         "e-mail, spreadsheet, RTF or image files)." + skipped)
    if embedding_model:
        model = resolve_vector_model(embedding_model)
    else:
        model = vector_model_for_path(read_config().get("EMBEDDING_MODEL_NAME"))
        if model is None:
            raise ValueError("Choose an embedding_model. " + " ".join(language_guidance()))
    waiting = staged_files()
    if waiting and not clear_waiting_files:
        raise ValueError(f"{len(waiting)} file(s) are already waiting to be added to a database from an earlier "
                         "session. Ask the user whether they may be removed from that waiting list (the files "
                         "themselves are not deleted), then call again with clear_waiting_files set to true.")
    return {
        "name": name,
        "paths": [str(p) for p in resolved],
        "files": len(files),
        "unsupported": len(selection.unsupported),
        "model": model,
        "download": not is_vector_model_downloaded(model),
    }


def start_build_job(name, paths, embedding_model=None, ocr_scanned_pdfs=False, clear_waiting_files=False):
    plan = plan_build(name, paths, embedding_model, clear_waiting_files)
    name = plan["name"]
    status = {
        "name": name,
        "state": "queued",
        "paths": plan["paths"],
        "model": plan["model"]["name"],
        "model_size_mb": plan["model"].get("size_mb"),
        "files": plan["files"],
        "ocr_scanned_pdfs": bool(ocr_scanned_pdfs),
        "clear_waiting_files": bool(clear_waiting_files),
        "started": time.time(),
        "finished": None,
        "pid": None,
        "process_started": None,
        "ocr": None,
        "progress": None,
        "message": "",
        "not_added": [],
    }
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    cancel_path(name).unlink(missing_ok=True)
    write_status(status)
    flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    try:
        with open(log_path(name), "w", encoding="utf-8") as log:
            subprocess.Popen(
                [sys.executable, "-m", "core.build_jobs", name],
                cwd=str(PROJECT_ROOT),
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"},
                creationflags=flags,
                start_new_session=sys.platform != "win32",
            )
    except OSError as e:
        status.update(state="failed", finished=time.time(), message=f"The build could not be started: {e}")
        write_status(status)
        raise ValueError(status["message"]) from None
    return plan


def request_cancel(name):
    status = read_status(name)
    if status is None or not job_is_running(status):
        raise ValueError(f"'{name}' is not being created right now.")
    cancel_path(name).touch()
    return f"Asked to stop creating '{name}'. Its partial files are removed once it stops."


def _ago(timestamp):
    return f"{format_duration(time.time() - timestamp)} ago" if timestamp else "a moment ago"


def _current_step(status):
    state = status.get("state")
    if state == "queued":
        return "starting"
    if state == "downloading":
        size = status.get("model_size_mb")
        return f"downloading the embedding model {status.get('model')}" + (f" (about {size} MB)" if size else "")
    if state == "adding":
        return "adding the files"
    if state == "ocr":
        ocr = status.get("ocr") or {}
        return f"making scanned PDFs searchable ({ocr.get('done', 0)} of {ocr.get('total', '?')} done)"
    from core.build_progress import STAGE_LABELS

    progress = status.get("progress") or {}
    stage = progress.get("stage")
    step = STAGE_LABELS.get(stage, "preparing").lower()
    if stage == "embed" and progress.get("batches"):
        step += f", batch {progress.get('batch') or 0} of {progress['batches']}"
    elif stage == "write":
        step = "saving the database"
    if progress.get("chunks"):
        step += f" ({progress['chunks']} chunks)"
    return step


def describe_status(status):
    name = status["name"]
    state = status.get("state")
    files = status.get("files")
    if state in ACTIVE_STATES and not job_is_running(status):
        return (f"Creating '{name}' stopped unexpectedly before it finished. Its log is {log_path(name)}. "
                "Try creating it again.")
    if state in ACTIVE_STATES:
        return (f"'{name}' is being created from {files} file(s) with {status.get('model')}: {_current_step(status)}. "
                f"Started {_ago(status.get('started'))}.")
    if state == "finished":
        duration = format_duration((status.get("finished") or time.time()) - (status.get("started") or time.time()))
        chunks = (status.get("progress") or {}).get("chunks")
        text = (f"'{name}' was created from {files} file(s) with {status.get('model')} in {duration}"
                + (f" ({chunks} chunks)" if chunks else "") + ". It can be searched now.")
        not_added = status.get("not_added") or []
        if not_added:
            shown = "; ".join(not_added[:SHOWN_NOT_ADDED])
            more = len(not_added) - SHOWN_NOT_ADDED
            text += f" {len(not_added)} file(s) were not fully added: {shown}" + (f"; and {more} more." if more > 0 else ".")
        return text
    if state == "cancelled":
        return f"Creating '{name}' was cancelled, and its partial files were removed."
    return f"Creating '{name}' failed: {status.get('message') or 'unknown error'}"


def status_report(name=None):
    from core.databases import list_databases
    from core.locks import busy_message, current_operation

    if name:
        status = read_status(name)
        if status is not None:
            return describe_status(status)
        if name in list_databases():
            return f"'{name}' exists and can be searched."
        return f"No database called '{name}' exists or is being created."
    running = running_job()
    if running is not None:
        return describe_status(running)
    holder = current_operation()
    if holder is not None:
        return busy_message(holder)
    statuses = all_statuses()
    if statuses:
        return describe_status(statuses[0])
    return "No database is being created, and none has been started from KoboldCpp yet."


class _Job:
    def __init__(self, name):
        self.name = name
        self.status = read_status(name)
        self.last_write = 0.0
        self.staged = False

    def update(self, force=True, **fields):
        self.status.update(fields)
        now = time.monotonic()
        if force or now - self.last_write >= 1.0:
            self.last_write = now
            write_status(self.status)

    def finish(self, state, message="", not_added=None):
        self.update(state=state, finished=time.time(), message=message, not_added=not_added or [])
        cancel_path(self.name).unlink(missing_ok=True)

    def cancel_requested(self):
        return cancel_path(self.name).exists()


def _log(text):
    print(text, flush=True)


def _run(job):
    from core.build_progress import BuildProgress
    from core.databases import DatabaseBuild, check_preconditions_for_db_creation
    from core.downloads import ModelDownloader, is_vector_model_downloaded, model_directory, resolve_vector_model
    from core.initialize import prepare
    from core.settings import set_embedding_model
    from core.staging import clear_staged_files, collect_files, stage_files, staged_files

    status = job.status
    prepare()
    model = resolve_vector_model(status["model"])
    if not is_vector_model_downloaded(model):
        job.update(state="downloading")
        _log(f"Downloading {model['name']}...")
        ModelDownloader(model, "vector").download()
    if job.cancel_requested():
        return job.finish("cancelled")
    set_embedding_model(model_directory(model))
    if staged_files():
        if not status.get("clear_waiting_files"):
            return job.finish("failed", "Files from an earlier session are waiting to be added. Call again with "
                                        "clear_waiting_files set to true to remove them from the waiting list.")
        clear_staged_files()
    job.update(state="adding")
    job.staged = True
    selection = collect_files([Path(p) for p in status["paths"]])
    made, errors = stage_files(selection.top_level + selection.nested)
    for error in errors:
        _log(error)
    if not staged_files():
        return job.finish("failed", "None of the files could be added" + (f": {errors[0]}" if errors else "."))
    job.update(files=len(staged_files()))
    if status.get("ocr_scanned_pdfs"):
        from core.ocr_tools import ocr_staged_pdfs

        job.update(state="ocr", ocr={"done": 0, "total": None})

        def on_start(index, total, source):
            _log(f"OCR {index}/{total}: {source}")
            job.update(ocr={"done": index - 1, "total": total})

        def on_result(index, total, source, output, error, events):
            _log(f"  {'saved ' + str(output) if output else 'failed: ' + str(error)}")
            job.update(ocr={"done": index, "total": total})

        ocr_staged_pdfs(on_start=on_start, on_result=on_result, should_stop=job.cancel_requested)
        if job.cancel_requested():
            clear_staged_files()
            return job.finish("cancelled")
    ok, message, _ = check_preconditions_for_db_creation(PROJECT_ROOT, job.name, skip_ocr=True)
    if not ok:
        clear_staged_files()
        return job.finish("failed", message)
    job.update(state="building")
    build = DatabaseBuild(job.name)
    progress = BuildProgress()
    finished = threading.Event()

    def watch_for_cancel():
        while not finished.wait(1.0):
            if job.cancel_requested():
                build.cancel()
                return

    def on_line(line):
        _log(line)
        if progress.feed(line):
            job.update(force=False, progress=progress.state())

    watcher = threading.Thread(target=watch_for_cancel, daemon=True)
    watcher.start()
    try:
        result = build.run(on_line)
    finally:
        finished.set()
    job.status["progress"] = progress.state()
    if result.success:
        return job.finish("finished", result.message, result.not_added)
    clear_staged_files()
    if result.cancelled:
        return job.finish("cancelled", result.message)
    last_lines = " | ".join(progress.log[-5:])
    return job.finish("failed", result.message + (f" Last log lines: {last_lines}" if last_lines else ""))


def run_job(name):
    from core.environment import prepare_process

    prepare_process(logging.WARNING)
    job = _Job(name)
    if job.status is None:
        _log(f"No status file for {name}")
        return 1
    job.update(pid=os.getpid(), process_started=_process_started(os.getpid()))
    from core.locks import BusyError, exclusive

    try:
        with exclusive(f"creating the database '{name}'"):
            _run(job)
    except BusyError as e:
        job.finish("failed", str(e))
    except Exception as e:
        traceback.print_exc()
        if job.staged:
            from core.staging import clear_staged_files

            clear_staged_files()
        job.finish("failed", f"{type(e).__name__}: {e}")
    return 0 if job.status.get("state") == "finished" else 1


if __name__ == "__main__":
    sys.exit(run_job(sys.argv[1]))
