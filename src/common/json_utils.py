import os
import json


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


def save_json(path: str, data, base_dir: str = None):
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
        print(f"Saved data to {json_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to save to {json_path}: {e}")
