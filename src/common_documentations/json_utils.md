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

## Best practices

- For production-level reliability consider writing to a temporary file and atomically renaming it into place to avoid partial writes.
- Validate that objects are JSON-serializable before calling `save_json` to produce clearer user errors.
- Prefer `pathlib.Path` for path manipulations in caller code; this module accepts string paths to remain simple.

