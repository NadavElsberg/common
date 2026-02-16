import requests

__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]


def get_first_imdb_title(name, print_error=False):
    """Get the IMDb title for a given production name.

    Uses IMDb's suggestion/search API to find a title matching the given name.

    Args:
        name (str): The production name to search for (e.g. "Inception", "Breaking Bad").

    Returns:
        the title ID (e.g. "tt1375666") if found for the first matching result, or None if not found or on error.
    """
    # Use IMDb's auto-suggest API (public, no API key needed)
    # It returns JSON with title suggestions matching the query
    search_url = f"https://v3.sg.media-imdb.com/suggestion/x/{requests.utils.quote(name)}.json"

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("d", [])
        if not results:
            return None

        # Filter to only title results with an id
        for result in results:
            if "id" in result:
                title_id = result.get("id", "")
                return title_id

        return None
    except requests.RequestException as e:
        if print_error:
            print(f"Error fetching IMDb title: {e}")
        return None
    

def get_imdb_title_info(name, print_error=False):
    """Get detailed IMDb title information for a given production name.

    Uses IMDb's suggestion/search API to find a title matching the given name.

    Args:
        name (str): The production name to search for (e.g. "Inception", "Breaking Bad").

    Returns:
        dict: A dictionary with title info for the first matching result, including 'id', 'title', 'year', 'type', and 'url',
              or None if no result is found or on error.
    """
    # Use IMDb's auto-suggest API (public, no API key needed)
    # It returns JSON with title suggestions matching the query
    search_url = f"https://v3.sg.media-imdb.com/suggestion/x/{requests.utils.quote(name)}.json"

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("d", [])
        if not results:
            return None

        # Filter to only title results (qid starting with 'movie', 'tvSeries', etc.)
        for result in results:
            qid = result.get("qid", "")
            if qid in ("movie", "tvSeries", "tvMovie", "tvMiniSeries", "short", "videoGame", "video"):
                title_id = result.get("id", "")
                return {
                    "id": title_id,
                    "title": result.get("l", ""),
                    "year": result.get("y", None),
                    "type": qid,
                    "url": f"https://www.imdb.com/title/{title_id}/" if title_id else None,
                }

        return None

    except requests.RequestException as e:
        if print_error:
            print(f"Error fetching IMDb title: {e}")
        return None