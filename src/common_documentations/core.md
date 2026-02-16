# core.py

## Overview

`core.py` contains lightweight utility helpers used across the `common` package. At present the module provides an email validation function and defines `__all__` to export public, callable symbols.

---

## Public API

### is_valid_email(email) -> bool

- **Description:** Validate whether a given string is a well-formed email address using a regular expression check.

- **Parameters:**
  - `email` (str): The email address string to validate.

- **Returns:**
  - `bool`: `True` if `email` matches the pattern `^[\w\.-]+@[\w\.-]+\.\w+$`, otherwise `False`.

- **Notes:**
  - The regex covers common email formats but is not fully RFC 5322 compliant. For strict validation consider a dedicated library such as `email-validator`.
  - The function uses `re.match`, so it anchors the check to the start of the string.

**Example**

```python
from common.core import is_valid_email

print(is_valid_email("user@example.com"))          # True
print(is_valid_email("not-an-email"))               # False
print(is_valid_email("name.last@sub.domain.org"))   # True
```

---

## Module details

- `__all__` is constructed dynamically at import time to include all names in the module's globals that do not start with `_` and are callable. This means only callables (functions, classes) will be exported by `from common.core import *` and internal helpers prefixed with `_` will be excluded.

---

## Contributing / Improvements

- For stricter email validation, consider integrating with the `email-validator` package or extending the regex to handle edge cases (quoted local parts, international domains, etc.).
- This module can be extended with additional commonly used validation or utility helpers.
