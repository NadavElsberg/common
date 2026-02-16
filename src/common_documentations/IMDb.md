# IMDb.py

## Overview

`IMDb.py` provides lightweight helpers for querying IMDb's public auto-suggest API to look up movie, TV series, and other production titles. No API key is required — the module uses IMDb's suggestion endpoint directly.

---

## Public API

### get_first_imdb_title(name: str, print_error: bool = False) -> str | None

- **Description:** Search IMDb for a production matching `name` and return the title ID (e.g. `"tt1375666"`) of the first result that has an `id` field.
- **Parameters:**
  - `name` (str): The production name to search for (e.g. `"Inception"`, `"Breaking Bad"`).
  - `print_error` (bool): If `True`, prints any request errors to stdout. Default `False`.
- **Returns:**
  - `str`: The IMDb title ID (e.g. `"tt1375666"`) of the first matching result.
  - `None`: If no results are found or a network error occurs.
- **Notes:**
  - This function returns the first result with an `id` regardless of its type (movie, person, etc.). If you need to filter by content type, use `get_imdb_title_info` instead.
  - Uses `requests.get` with a 10-second timeout.

**Example**

```python
from common.IMDb import get_first_imdb_title

title_id = get_first_imdb_title("Inception")
print(title_id)  # e.g. "tt1375666"
```

---

### get_imdb_title_info(name: str, print_error: bool = False) -> dict | None

- **Description:** Search IMDb for a production matching `name` and return detailed information for the first result whose type matches a known content category.
- **Parameters:**
  - `name` (str): The production name to search for (e.g. `"Inception"`, `"Breaking Bad"`).
  - `print_error` (bool): If `True`, prints any request errors to stdout. Default `False`.
- **Returns:**
  - `dict` with the following keys:
    - `id` (str): IMDb title ID (e.g. `"tt1375666"`).
    - `title` (str): Display title as returned by IMDb.
    - `year` (int | None): Release year, or `None` if unavailable.
    - `type` (str): Content type — one of `"movie"`, `"tvSeries"`, `"tvMovie"`, `"tvMiniSeries"`, `"short"`, `"videoGame"`, `"video"`.
    - `url` (str | None): Full IMDb URL (e.g. `"https://www.imdb.com/title/tt1375666/"`).
  - `None`: If no matching title is found or a network error occurs.
- **Notes:**
  - Only results with a recognised `qid` (content type) are returned; person results and other non-title entries are skipped.
  - Uses `requests.get` with a 10-second timeout.

**Example**

```python
from common.IMDb import get_imdb_title_info

info = get_imdb_title_info("Breaking Bad")
if info:
    print(info["title"])  # "Breaking Bad"
    print(info["year"])   # 2008
    print(info["type"])   # "tvSeries"
    print(info["url"])    # "https://www.imdb.com/title/tt0903747/"
```

---

## Module details

- `__all__` is constructed dynamically at import time to include all names in the module's globals that do not start with `_` and are callable.
- The module depends on the `requests` library. Ensure it is installed (`pip install requests`).
- Both functions use the public IMDb auto-suggest endpoint (`https://v3.sg.media-imdb.com/suggestion/x/<query>.json`), which does not require authentication but is an unofficial API and may change without notice.

---

## Contributing / Improvements

- Consider caching results to avoid redundant network calls for repeated queries.
- Add support for returning multiple results instead of just the first match.
- The auto-suggest endpoint is undocumented and subject to change; for production use consider the official IMDb API or OMDb API.
