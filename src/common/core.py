import re
import time
import requests


__all__ = [
    name for name in globals()
    if not name.startswith("_")
    and callable(globals()[name])
]




def is_valid_email(email):
    """Validate an email address using a regular expression."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

