# formating.py

## Overview

`formating.py` provides a collection of small utilities for formatting numeric values, byte sizes, and durations, plus a couple of convenience utilities for quick printing and input parsing. These helpers are intended for quick scripting and CLI usage.

---

## Public API

### show_as_10th_power(num: int, length_to_return_string: int = 2) -> str | tuple

- **Description:** Convert an integer to a short «scientific-like» string of the form `a*10^b` when the number of digits exceeds `length_to_return_string`. If the number is short enough it's returned as a plain string.
- **Parameters:**
  - `num` (int): The number to represent.
  - `length_to_return_string` (int): Threshold of digits above which the condensed form is returned. Default 2.
- **Returns:**
  - If the number has <= `length_to_return_string` digits, returns the plain string representation.
  - Otherwise returns a tuple `(string_Answer, first_digit, power)` where `string_Answer` is `"{first_digit}*10^{power}"`.
- **Example:** `show_as_10th_power(123456789012)` -> `('1*10^11', 1, 11)`
- **Notes / caveats:** The function falls back to an exception handler that currently returns a numeric estimate of digit length in some error conditions.

---

### add_Commas(num) -> str

- **Description:** Return a string representation of `num` with commas as thousands separators.
- **Parameters:**
  - `num` (int | float | any): Value to format. If formatting fails, the function will return `str(num)`.
- **Returns:** `str` with comma formatting or fallback string.
- **Example:** `add_Commas(1234567)` -> `'1,234,567'`

---

### print_tuples(tup)

- **Description:** Prints each element of a tuple on its own line with a prefix, then prints the whole tuple.
- **Parameters:** `tup` (iterable)
- **Returns:** None (prints to stdout).

---

### get_input_list(prompt: str, type_cast: type = int) -> list

- **Description:** Read a comma-separated input from stdin using `input()` and cast each entry to `type_cast`.
- **Parameters:**
  - `prompt` (str): Prompt shown to the user.
  - `type_cast` (type): Callable used to convert each piece (defaults to `int`).
- **Returns:** List of converted values.
- **Usage note:** This helper is convenient for quick CLI scripts but has no validation beyond the `type_cast` call.

---

### bytes_format_string(num_bytes: int, inputsuffix: str = 'B', outputsuffix: str = 'B', show_conversion: bool = False) -> str

- **Description:** Convert a quantity expressed in `inputsuffix` into a human-friendly string with units (e.g., `1.23 MB`). Supports B, KB, MB, GB, TB, PB using multiples of 1024.
- **Parameters:**
  - `num_bytes` (int | float): Numeric value of bytes to convert.
  - `inputsuffix` (str): Suffix in which `num_bytes` is expressed (default `'B'`).
  - `outputsuffix` (str): Desired output suffix (default `'B'`). If omitted, function chooses the most appropriate suffix.
  - `show_conversion` (bool): If True, prints the conversion details to stdout.
- **Returns:** String of the form `"<value> <suffix>"` (rounded to two decimals).
- **Example:** `bytes_format_string(1536)` -> `'1.50 KB'`

---

### bytes_format_tuple(num_bytes: int, inputsuffix: str = 'B', outputsuffix: str = 'B', show_conversion: bool = False) -> tuple

- **Description:** Same conversion as `bytes_format_string` but returns a tuple `(value, suffix)` instead of a string.
- **Example:** `bytes_format_tuple(2048)` -> `(2.0, 'KB')`

---

### duration_format_string(length: int, input_unit: str, output_unit: str, show_conversion: bool = False) -> str

- **Description:** Convert a duration expressed in `input_unit` to `output_unit` and return a human-readable string with two decimals.
- **Supported units:** `seconds`, `minutes`, `hours`, `days`, `weeks`.
- **Example:** `duration_format_string(120, 'seconds', 'minutes')` -> `'2.00 minutes'`

---

### duration_format_tuple(length: int, input_unit: str, output_unit: str, show_conversion: bool = False) -> tuple

- **Description:** Same as `duration_format_string` but returns `(value, unit)` as a tuple.

---

## Notes & best practices

- These helpers are intentionally small and designed for scripting and quick CLI usage. For production code consider:
  - Robust validation of inputs.
  - Returning structured data (e.g., numeric results) and formatting in the presentation layer.
  - Adding unit tests for boundary conditions (very large/small numbers, negative values, invalid suffixes).

---

## Examples

```python
from common.formating import bytes_format_string, duration_format_string

print(bytes_format_string(15634567))           # -> '14.91 MB'
print(duration_format_string(3600, 'seconds', 'hours'))  # -> '1.00 hours'
```
