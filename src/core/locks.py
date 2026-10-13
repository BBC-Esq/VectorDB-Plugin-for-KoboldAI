import json
import os
import time
from contextlib import contextmanager

from filelock import FileLock, Timeout

from core.constants import PROJECT_ROOT

BUSY_LOCK_PATH = PROJECT_ROOT / "busy.lock"
BUSY_INFO_PATH = PROJECT_ROOT / "busy.json"
CONFIG_LOCK_PATH = PROJECT_ROOT / "config.lock"

_busy_lock = FileLock(str(BUSY_LOCK_PATH))
config_lock = FileLock(str(CONFIG_LOCK_PATH), timeout=60)


class BusyError(RuntimeError):
    pass


def _read_info():
    try:
        info = json.loads(BUSY_INFO_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return info if isinstance(info, dict) else None


def busy_message(info):
    if not info:
        return "Another operation is still running. Try again when it finishes."
    minutes = max(0, int((time.time() - info.get("started", time.time())) // 60))
    since = "less than a minute ago" if minutes < 1 else f"{minutes} minute(s) ago"
    return (f"The program is busy {info.get('operation', 'with another operation')} "
            f"(process {info.get('pid', '?')}, started {since}). Try again when it finishes.")


def current_operation():
    if _busy_lock.is_locked:
        return _read_info()
    try:
        _busy_lock.acquire(timeout=0)
    except Timeout:
        return _read_info() or {}
    _busy_lock.release()
    return None


@contextmanager
def exclusive(operation):
    nested = _busy_lock.is_locked
    try:
        _busy_lock.acquire(timeout=0)
    except Timeout:
        raise BusyError(busy_message(_read_info())) from None
    try:
        if not nested:
            BUSY_INFO_PATH.write_text(
                json.dumps({"pid": os.getpid(), "operation": operation, "started": time.time()}),
                encoding="utf-8",
            )
        yield
    finally:
        if not nested:
            try:
                BUSY_INFO_PATH.unlink()
            except OSError:
                pass
        _busy_lock.release()
