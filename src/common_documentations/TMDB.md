# TMDB.py

## Overview

`TMDB.py` provides helpers for searching TMDB for movies and TV shows. TMDB requires an API key. Supply it as the `api_key` argument or set the `TMDB_API_KEY` environment variable; never commit the key to source control.

## Public API

### get_first_tmdb_title(name: str, print_error: bool = False, api_key: str | None = None) -> int | None

Searches movies and TV shows and returns the TMDB ID of the first matching title. Returns `None` if no title is found or the request fails.

### get_tmdb_title_info(name: str, print_error: bool = False, api_key: str | None = None) -> dict | None

Returns details for the first matching movie or TV show:

- `id`: numeric TMDB ID.
- `title`: display title.
- `year`: release/first-air year, or `None` if unavailable.
- `type`: `movie` or `tv`.
- `url`: title page on themoviedb.org.
- `imageUrl`: full-size poster URL, or `None` if unavailable.

### get_tmdb_look_up(name: str, print_error: bool = False, api_key: str | None = None) -> list[int] | None

Returns a list of IDs for matching movies and TV shows, or `None` when no matches are found. This is the TMDB equivalent of `get_imdb_look_up`.

### get_tmdb_title_image(title_id: int | str, print_error: bool = False, api_key: str | None = None) -> str | None

Looks up a title by its TMDB ID and returns its full-size poster URL, or `None` if it is unavailable. The helper checks movie and TV details endpoints.

## Example

```python
import os
from common.TMDB import get_tmdb_title_info, get_first_tmdb_title

# Set TMDB_API_KEY in your environment before running this example.
info = get_tmdb_title_info("Inception")
tmdb_id = get_first_tmdb_title("Inception")
print(info)
print(tmdb_id)
```

The helpers use TMDB's `/search/multi` endpoint, which includes both movies and TV shows. Person results are excluded. HTTP requests use a 10-second timeout. TMDB's API and image URLs are subject to TMDB's terms and image usage guidelines.
