# common
A collection of small, reusable Python utilities intended for use across projects. Each module focuses on a specific area (formatting, JSON helpers, math utilities, network checks, etc.).

## Documentation
The `src/common_documentations` directory contains detailed documentation for each module:

- [core](src/common_documentations/core.md) — basic utilities (e.g., email validation).
- [formating](src/common_documentations/formating.md) — helpers to format numbers, bytes, and durations.
- [IMDb](src/common_documentations/IMDb.md) — IMDb title lookup helpers using the public auto-suggest API.
- [json_utils](src/common_documentations/json_utils.md) — safe and simple JSON file load/save helpers.
- [math](src/common_documentations/math.md) — primality and numeric utilities, ID checksum functions.
- [network](src/common_documentations/network.md) — network utilities: ping, IP discovery, port checks.
- [wrappers](src/common_documentations/wrappers.md) — reusable decorators for logging and timing.

## Quick start
2 ways to get started with the package:
 1) Download the "install.bat"/"install.sh" file up aove and run it. this should get your default python installations and run put the dir there.
 2) Proceed to this installation procces as such:
  - clone the packege
  - cd to the destination dir
  - then run: "pip install -e ." in the dir you cloned the repo to.

for example{on a windows machine}: 
```batch
git clone https://github.com/NadavElsberg/common.git c:/common
cd c:/common
pip install -e .
```


example of use of code
```python
from common.formating import bytes_format_string
print(bytes_format_string(2048))  # -> '2.00 KB'
```

## License
This project is licensed under the MIT License — see the `LICENSE` file for details.

## Contributing
Contributions are welcome — please contact the developer via the Email address mentioned to get on the go
