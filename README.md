# common
A collection of small, reusable Python utilities intended for use across projects. Each module focuses on a specific area (formatting, JSON helpers, math utilities, network checks, etc.).

## Documentation
The `src/common_documentations` directory contains detailed documentation for each module:

- [core](src/common_documentations/core.md) — basic utilities and decorators (e.g., `countTime`).
- [formating](src/common_documentations/formating.md) — helpers to format numbers, bytes, and durations.
- [json_utils](src/common_documentations/json_utils.md) — safe and simple JSON file load/save helpers.
- [math](src/common_documentations/math.md) — primality and numeric utilities, ID checksum functions.
- [network](src/common_documentations/network.md) — network utilities: ping, IP discovery, port checks.

## Quick start
Install the package (if packaged) or add this repo to your `PYTHONPATH` and import utilities from `common`:

```python
from common.formating import bytes_format_string
print(bytes_format_string(2048))  # -> '2.00 KB'
```

## Contributing
Contributions are welcome — please open issues or PRs with tests and documentation updates.
