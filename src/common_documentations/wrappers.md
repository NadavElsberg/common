# wrappers.py

## Overview

`wrappers.py` provides reusable function decorators for common cross-cutting concerns such as logging and timing. These decorators are designed as lightweight building blocks that can be applied to any callable.

---

## Public API

### baseWrapper(func)

- **Type:** decorator
- **Description:** A general-purpose wrapper that logs the function name, arguments, and return value to stdout before and after each call. Useful as a debugging/tracing decorator or as a template for building custom wrappers.

- **Parameters:**
  - `func` (callable): The function to be wrapped.

- **Returns:**
  - `wrapper` (callable): The wrapped function which prints call details and return values.

- **Behavior:**
  - Before calling `func`, prints: `Calling function '<name>' with args: (...) and kwargs: {...}`
  - After calling `func`, prints: `Function '<name>' returned: <result>`
  - The original return value is passed through unchanged.

- **Notes:**
  - The decorator does not preserve the wrapped function's metadata (`__name__`, `__doc__`). Consider applying `functools.wraps(func)` to the inner `wrapper` if that matters.
  - Exceptions raised by the wrapped function propagate through unchanged.

**Example**

```python
from common.wrappers import baseWrapper

@baseWrapper
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
# prints: Calling function 'greet' with args: ('Alice',) and kwargs: {}
# prints: Function 'greet' returned: Hello, Alice!
```

---

### countTime(func)

- **Type:** decorator
- **Description:** A timing decorator that measures the wall-clock execution time of a function and prints it to stdout. Returns the function's original return value unchanged.

- **Parameters:**
  - `func` (callable): The function to be wrapped.

- **Returns:**
  - `wrapper` (callable): The wrapped function which prints execution time when invoked.

- **Behavior:**
  - Uses `time.time()` to capture start and end timestamps around the function call.
  - Prints a message of the form: `Function '<name>' executed in <seconds> seconds.`

- **Notes:**
  - The decorator does not preserve the wrapped function's metadata — consider using `functools.wraps` if that is important.
  - Exceptions raised by the wrapped function propagate through unchanged.
  - The current implementation captures `end_time` before calling the function — this is a known ordering issue that may result in near-zero timings. A fix would move the `end_time` capture to after the `func()` call.

**Example**

```python
from common.wrappers import countTime

@countTime
def work(n):
    import time
    time.sleep(n)
    return n * 2

result = work(0.5)  # prints: Function 'work' executed in ~0.5 seconds.
```

---

## Module details

- `__all__` is constructed dynamically at import time to include all names in the module's globals that do not start with `_` and are callable. This means only callables (functions, classes) will be exported by `from common.wrappers import *` and internal helpers prefixed with `_` will be excluded.

---

## Contributing / Improvements

- Wrap the inner `wrapper` with `functools.wraps(func)` to preserve function metadata for both decorators.
- Fix the timing order in `countTime` so `end_time` is captured after `func()` finishes.
- Consider adding additional decorators such as `retry`, `memoize`, or `log_to_logger` that logs to a `logging.Logger` instead of printing.
