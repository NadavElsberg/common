# math.py

## Overview

`math.py` contains a set of numerical and utility functions that are useful across projects: primality checks, ID control-digit computation, matrix printing helpers, and small printing helpers.

---

## Public API

### is_prime(n: int) -> bool

- **Description:** Determine if `n` is a prime number using trial division optimized by checking up to sqrt(n) and skipping multiples of 2/3.
- **Parameters:**
  - `n` (int): Value to test for primality.
- **Returns:** `True` if `n` is prime, `False` otherwise.
- **Example:** `is_prime(7)` -> `True`

---

### is_allmost_prime(n: int) -> bool

- **Description:** Test whether `n` is an "almost prime" — defined here as a product of exactly two prime factors (counted with multiplicity).
- **Parameters:** `n` (int)
- **Returns:** `True` if `n` is the product of exactly two primes, otherwise `False`.
- **Notes:** This routine factors by trial division and counts prime factors.

---

### print_matrix(M)

- **Description:** Utility to print a 2D matrix (list of lists) with each element and its coordinates.
- **Parameters:** `M` (list[list])
- **Returns:** None (prints to stdout)

---

### print_tuples(tup)

- **Description:** Print each item from an iterable with a small prefix and then print the entire structure.
- **Parameters:** `tup` (iterable)
- **Returns:** None (prints to stdout)

---

### control_digit(id_num)

- **Description:** Compute the control digit for an 8-digit identity base using an algorithm that doubles every second digit from the right (with checksum-like logic) and returns the calculated final single digit as a string.
- **Parameters:** `id_num` (str): Expect exactly 8 digits.
- **Returns:** `str`: Single digit representing control checksum.
- **Raises:** AssertionError if input is not a str of length 8.

---

### audit_ID(IDNumber: str) -> bool

- **Description:** Validate a full 9-character ID where the last digit is the checksum digit computed by `control_digit`.
- **Parameters:** `IDNumber` (str): 9-character numeric string.
- **Returns:** `True` if valid, `False` otherwise.

---

## Examples

```python
from common.math import is_prime, is_allmost_prime, audit_ID

print(is_prime(97))            # True
print(is_allmost_prime(21))    # True (3 * 7)
print(audit_ID('123456782'))   # Example: depends on checksum
```

---

## Notes

- Input validation is minimal to keep these helpers lightweight; callers should validate types where appropriate.
- Consider adding unit tests for edge cases and negative inputs.
