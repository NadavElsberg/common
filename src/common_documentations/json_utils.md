# json_utils.py

## Overview

`json_utils.py` contains small, safe helpers for loading and saving JSON files. The functions handle common filesystem concerns (relative vs absolute paths) and wrap lower-level exceptions with clearer messages.

---

## Public API

### get_json(path: str, base_dir: str = None)

- **Description:** Load JSON data from `path` and return the parsed Python object.
- **Parameters:**
  - `path` (str): Path to the JSON file. Can be absolute or relative.
  - `base_dir` (str | None): Base directory to join with `path` if `path` is relative. Defaults to the current working directory (`os.getcwd()`).
- **Behavior:**
  - If `path` is absolute, it will be used as-is.
  - If the file does not exist, the function returns an empty list (`[]`).
  - If the file exists but contains invalid JSON, a `RuntimeError` describing the parse failure is raised.
- **Returns:** Parsed JSON Python object (e.g., dict or list).

**Example**

```python
from common.json_utils import get_json

data = get_json('data/config.json', base_dir='/project')
```

---

### save_json(path: str, data, base_dir: str = None)

- **Description:** Save `data` as JSON to `path`. Creates the target directory if required and writes with UTF-8 encoding and an indent of 4 spaces.
- **Parameters:**
  - `path` (str): Target file path. Can be absolute or relative.
  - `data` (any): JSON-serializable Python object to save.
  - `base_dir` (str | None): Base directory to join with `path` when `path` is relative. Defaults to the current working directory.
- **Behavior:**
  - Ensures parent directories are created using `os.makedirs(..., exist_ok=True)`.
  - Writes the file in UTF-8 with `json.dump(..., ensure_ascii=False, indent=4)`.
  - Prints a confirmation message `Saved data to <path>` on success.
  - On unexpected errors (IO errors, type errors from non-serializable objects, etc.) the function raises a `RuntimeError` with details.

**Example**

```python
from common.json_utils import save_json

save_json('out/results.json', {'ok': True})
```

---

## New / advanced helpers

### atomic_save_json(path: str, obj)

- **Description:** Atomically write `obj` as JSON to `path` by writing to a temporary file in the same directory, flushing & syncing, then replacing the destination file.
- **Parameters:**
  - `path` (str): Destination file path.
  - `obj` (any): JSON-serializable object to save.
- **Behavior:**
  - Uses a temporary file in the destination directory and `os.replace()` so the final rename is atomic on most filesystems.
  - Reduces the risk of partial files after crashes or process termination.
- **Returns:** `None`.

**Example**

```python
from common.json_utils import atomic_save_json
atomic_save_json('data/state.json', {'counter': 42})
```

---

### read_json_safe(path: str, default: Any = None, *, max_size: int = 5_000_000, raise_on_error: bool = False)

- **Description:** Read JSON from `path` and handle common error cases gracefully.
- **Parameters:**
  - `path` (str): File path to read.
  - `default` (Any): Value to return if the file is missing or a non-fatal error occurs (default: `None`).
  - `max_size` (int): Maximum file size in bytes to read; larger files return `default` unless `raise_on_error` is `True`.
  - `raise_on_error` (bool): When `True`, malformed JSON or oversized files raise `RuntimeError` instead of returning `default`.
- **Returns:** Parsed JSON object or `default`.

**Example**

```python
from common.json_utils import read_json_safe
cfg = read_json_safe('config.json', default={})
```

---

### atomic_update(path: str, updater_fn: Callable[[Any], Any], *, max_retries: int = 5, retry_delay: float = 0.1, read_default: Any = None) -> Any

- **Description:** Load JSON, call `updater_fn(current)` to compute a new value, then write it atomically. Retries if concurrent modifications are detected.
- **Parameters:**
  - `path` (str): Path to the JSON file.
  - `updater_fn` (Callable): Function that receives the current object and returns the updated object.
  - `max_retries` (int): Number of retries on detected conflicts (default 5).
  - `retry_delay` (float): Seconds to wait between retries (default 0.1).
  - `read_default` (Any): Value to use when the file is missing.
- **Returns:** The object that was written to disk.
- **Raises:** `RuntimeError` if the updater returns `None` or retries are exhausted.

**Example (increment a counter)**

```python
from common.json_utils import atomic_update

def inc_counter(obj):
    obj = obj or {}
    obj['count'] = obj.get('count', 0) + 1
    return obj

new = atomic_update('data/counter.json', inc_counter, read_default={})
```

---

### compute_etag(obj_or_path) -> str

- **Description:** Compute a stable SHA-256 hex digest for either a file's bytes (when `obj_or_path` is a path string) or for a JSON-canonical representation of a Python object.
- **Parameters:**
  - `obj_or_path` (str | any): File path or JSON-serializable object.
- **Returns:** Hexadecimal SHA-256 string.
- **Notes:** For objects, the function uses `json.dumps(..., sort_keys=True, separators=(",", ":"))` to ensure determinism.

**Example**

```python
from common.json_utils import compute_etag
print(compute_etag('data/config.json'))
print(compute_etag({'a': 1, 'b': 2}))
```

---

### backup_json(path: str, *, keep: int = 5, backup_dir: Optional[str] = None) -> str

- **Description:** Copy `path` to a timestamped backup file and rotate older backups to keep only the most recent `keep` files.
- **Parameters:**
  - `path` (str): File to back up.
  - `keep` (int): Number of backups to retain (default 5).
  - `backup_dir` (Optional[str]): Directory to place backups (defaults to source file directory).
- **Returns:** Path to the created backup file.

**Example**

```python
from common.json_utils import backup_json
bk = backup_json('data/state.json', keep=3)
print('backup created at', bk)
```

---

## Best practices

- For production-level reliability consider writing to a temporary file and atomically renaming it into place to avoid partial writes.
- Validate that objects are JSON-serializable before calling `save_json` to produce clearer user errors.
- Prefer `pathlib.Path` for path manipulations in caller code; this module accepts string paths to remain simple.

