"""Helpers for searching The Movie Database (TMDB).

Set the ``TMDB_API_KEY`` environment variable or pass ``api_key`` to each
function. TMDB API keys are credentials; do not commit them to source control.
"""

import os

import requests

_API_BASE_URL = "https://api.themoviedb.org/3"
_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"
_TITLE_TYPES = {"movie", "tv"}


def _get_api_key(api_key):
    return api_key or os.getenv("TMDB_API_KEY")


def _search_titles(name, api_key, print_error):
    key = _get_api_key(api_key)
    if not key:
        if print_error:
            print("TMDB API key is required. Pass api_key or set TMDB_API_KEY.")
        return []

    try:
        response = requests.get(
            f"{_API_BASE_URL}/search/multi",
            params={"query": name, "api_key": key},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        return [result for result in results if result.get("media_type") in _TITLE_TYPES]
    except requests.RequestException as error:
        if print_error:
            print(f"Error fetching TMDB title: {error}")
        return []


def get_first_tmdb_title(name, print_error=False, api_key=None):
    """Return the first matching movie or TV show TMDB ID, or ``None``.

    Args:
        name (str): Production name to search for.
        print_error (bool): Print request or missing-key errors when true.
        api_key (str | None): TMDB API key. Defaults to the ``TMDB_API_KEY``
            environment variable.

    Returns:
        int | None: The first matching TMDB ID, or ``None`` if no title is found.
    """
    results = _search_titles(name, api_key, print_error)
    return results[0].get("id") if results else None


def get_tmdb_title_info(name, print_error=False, api_key=None):
    """Return details for the first matching TMDB movie or TV show.

    The result includes ``id``, ``title``, ``year``, ``type``, ``url``, and
    ``imageUrl``. ``type`` is either ``"movie"`` or ``"tv"``.
    """
    results = _search_titles(name, api_key, print_error)
    if not results:
        return None

    result = results[0]
    media_type = result["media_type"]
    title = result.get("title") or result.get("name", "")
    release_date = result.get("release_date") or result.get("first_air_date") or ""
    image_path = result.get("poster_path") or result.get("backdrop_path")

    return {
        "id": result.get("id"),
        "title": title,
        "year": int(release_date[:4]) if release_date[:4].isdigit() else None,
        "type": media_type,
        "url": f"https://www.themoviedb.org/{media_type}/{result['id']}"
        if result.get("id") is not None else None,
        "imageUrl": f"{_IMAGE_BASE_URL}{image_path}" if image_path else None,
    }


def get_tmdb_look_up(name, print_error=False, api_key=None):
    """Return all matching movie and TV show TMDB IDs, or ``None``.

    This mirrors ``get_imdb_look_up``: matching IDs are returned as a list;
    no results or a failed request returns ``None``.
    """
    results = _search_titles(name, api_key, print_error)
    title_ids = [result.get("id") for result in results if result.get("id") is not None]
    return title_ids or None


def get_tmdb_title_image(title_id, print_error=False, api_key=None):
    """Return a full-size poster image URL for a TMDB movie or TV show ID.

    TMDB requires the title type for its details endpoint, so the function
    tries both the movie and TV endpoints. Returns ``None`` if no poster is
    available or the title cannot be retrieved.
    """
    key = _get_api_key(api_key)
    if not key:
        if print_error:
            print("TMDB API key is required. Pass api_key or set TMDB_API_KEY.")
        return None

    for media_type in ("movie", "tv"):
        try:
            response = requests.get(
                f"{_API_BASE_URL}/{media_type}/{title_id}",
                params={"api_key": key},
                timeout=10,
            )
            if response.status_code == 404:
                continue
            response.raise_for_status()
            image_path = response.json().get("poster_path")
            return f"{_IMAGE_BASE_URL}{image_path}" if image_path else None
        except requests.RequestException as error:
            if print_error:
                print(f"Error fetching TMDB title image: {error}")
            return None

    return None


__all__ = [
    name for name in globals()
    if not name.startswith("_") and callable(globals()[name])
]
