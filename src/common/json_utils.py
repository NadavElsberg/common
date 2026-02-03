import os
import json
import tempfile
import hashlib
from typing import Any, Optional, Callable
import time
import shutil

__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]


def get_json(path: str, base_dir: str = None):
    """Load JSON from a path."""
    if os.path.isabs(path):
        json_path = path
    else:
        if base_dir is None:
            base_dir = os.getcwd()
        json_path = os.path.join(base_dir, path)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse {json_path}: {e}")


def save_json(path: str, data, base_dir: str = None, writepath: bool = True):
    """Save JSON to a path."""
    if os.path.isabs(path):
        json_path = path
    else:
        if base_dir is None:
            base_dir = os.getcwd()
        json_path = os.path.join(base_dir, path)

    try:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if writepath:
            print(f"Saved JSON to {json_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to save to {json_path}: {e}")


def atomic_save_json(path, obj):
    d = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=d)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def read_json_safe(path: str, default: Any = None, *, max_size: int = 5_000_000, raise_on_error: bool = False) -> Any:
    """Read JSON from `path`. Returns `default` if missing or too large.

    If JSON is malformed and `raise_on_error` is True, raises RuntimeError.
    """
    try:
        size = os.path.getsize(path)
        if size > max_size:
            if raise_on_error:
                raise RuntimeError(f"File too large: {path} ({size} bytes)")
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        if raise_on_error:
            raise RuntimeError(f"Failed to parse {path}: {e}")
        return default


def atomic_update(path, updater_fn):
    obj = read_json_safe(path, default={})
    new = updater_fn(obj)
    atomic_save_json(path, new)
    return new


def compute_etag(obj):
    s = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(s).hexdigest()


def compute_etag(obj_or_path) -> str:
    """Return hex sha256 for a file path (reads bytes) or Python object (canonical JSON)."""
    if isinstance(obj_or_path, str) and os.path.exists(obj_or_path):
        h = hashlib.sha256()
        with open(obj_or_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    # canonical JSON for stable hashing
    blob = json.dumps(obj_or_path, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def atomic_update(path: str, updater_fn: Callable[[Any], Any], *, max_retries: int = 5, retry_delay: float = 0.1, read_default: Any = None) -> Any:
    """Load JSON, call updater_fn(current)->new, then write atomically.

    Retries if concurrent modification detected (naive optimistic retry).
    Returns the new object.
    """
    for attempt in range(max_retries):
        current = read_json_safe(path, default=read_default)
        new = updater_fn(json.loads(json.dumps(current)))  # deep copy via dump/load
        if new is None:
            raise RuntimeError("updater_fn must return the new object")
        old_etag = compute_etag(current)
        new_etag = compute_etag(new)
        if old_etag == new_etag:
            return new  # nothing changed
        atomic_save_json(path, new)
        latest = read_json_safe(path, default=read_default)
        if compute_etag(latest) == new_etag:
            return new
        time.sleep(retry_delay)
    raise RuntimeError("Failed to update JSON after retries")


def backup_json(path: str, *, keep: int = 5, backup_dir: Optional[str] = None) -> str:
    """Copy `path` to a timestamped backup file and keep newest `keep` backups."""
    if backup_dir is None:
        backup_dir = os.path.dirname(path) or "."
    os.makedirs(backup_dir, exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%S")
    name = os.path.basename(path)
    backup_name = f"{name}.{ts}.bak"
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(path, backup_path)
    # rotate
    entries = [p for p in os.listdir(backup_dir) if p.startswith(name + ".") and p.endswith(".bak")]
    entries.sort(reverse=True)
    for old in entries[keep:]:
        try:
            os.remove(os.path.join(backup_dir, old))
        except Exception:
            pass
    return backup_path


