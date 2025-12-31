# core.py

## Overview

`core.py` contains lightweight utility helpers used across the `common` package. At present the module provides a single decorator to measure and report the execution time of a call and defines `__all__` to export public, callable symbols.

---

## Public API

### countTime(func)

- **Type:** decorator
- **Description:** A simple timing decorator that measures how long a function takes to execute and prints the elapsed time to stdout. The decorator returns the function's original return value unchanged.

- **Parameters:**
  - `func` (callable): The function to be wrapped.

- **Returns:**
  - `wrapper` (callable): The wrapped function which prints execution time when invoked.

- **Notes:**
  - The decorator prints a message of the form: `Function '<name>' executed in <seconds> seconds.` using `time.time()` to measure elapsed wall-clock time.
  - The decorator makes no attempt to preserve the wrapped function's metadata (such as `__name__`, `__doc__`) — consider using `functools.wraps` if that is important.
  - Exceptions raised by the wrapped function propagate through unchanged.

**Example**

```python
from common.core import countTime

@countTime
def work(n):
    import time
    time.sleep(n)
    return n * 2

# When you call work(0.5), you will see a printed timing line and get 1.0 as return
result = work(0.5)  # prints: Function 'work' executed in 0.500123 seconds.
```

---

## Module details

- `__all__` is constructed dynamically at import time to include all names in the module's globals that do not start with `_` and are callable. This means only callables (functions, classes) will be exported by `from common.core import *` and internal helpers prefixed with `_` will be excluded.

---

## Contributing / Improvements

- If you need to preserve function metadata for decorated functions, wrap the `wrapper` with `functools.wraps(func)`.
- You could extend this module with additional commonly used decorators (e.g., `retry`, `memoize`) or timing utilities that optionally log to a logger instead of printing.
