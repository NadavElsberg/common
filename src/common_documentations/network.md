# network.py

## Overview

`network.py` contains convenient network-related helper functions for pinging, discovering local and public IP addresses, and checking port availability. Functions are conservative (they catch many errors) and aimed at scripting and quick diagnostic tasks.

---

## Public API

### ping_host(host: str, count: int = 4, timeout: int = 2) -> tuple[bool, str]

- **Description:** Execute the system `ping` command against `host` and return a tuple `(is_reachable, output)` where `output` is the captured stdout/stderr.
- **Parameters:**
  - `host` (str): Hostname or IP address.
  - `count` (int): Number of ping packets to send (default 4).
  - `timeout` (int): Timeout per packet in seconds (default 2).
- **Returns:** `(bool, str)` — `True` when ping exit code is 0, otherwise `False`.
- **Notes:** Uses `subprocess.run` and handles platform differences (Windows vs others). If the `ping` utility is not found it returns `(False, "ping utility not found")`.

---

### ping(host: str, timeout: int = 2, count: int = 1) -> bool

- **Description:** Convenience wrapper around `ping_host` returning only a boolean reachability indicator.

---

### am_I_online(timeout: int = 5) -> bool

- **Description:** Quick internet connectivity check by attempting to ping well-known DNS servers (`1.1.1.1`, `8.8.8.8`, `9.9.9.9`). Returns `True` as soon as one server responds.
- **Parameters:** `timeout` (int)
- **Notes:** The function is implemented in `network.py` as `am_I_online` (some older docs or references may call this `is_online`).

---

### get_local_ip() -> str

- **Description:** Determine the machine's preferred outbound IP by opening a UDP socket to a public address (no packets sent). Returns `"0.0.0.0"` on error.

---

### get_public_ip(timeout: int = 5) -> str

- **Description:** Query public IP address from a list of public endpoints and return the first successful result. Returns `"0.0.0.0"` on failure.
- **Endpoints:** `https://api.ipify.org?format=json`, `https://ifconfig.me/ip`, `https://ipinfo.io/ip`.

---

### get_mac_address() -> str

- **Description:** Return the machine's MAC address formatted as a colon-separated hex sequence (e.g., `00:1a:2b:...`). Falls back to `00:00:00:00:00:00` on failure.

---

### is_port_open(host: str, port: int, timeout: float = 1.0, returntuple: bool = False) -> bool | tuple[bool,str]

- **Description:** Check whether a TCP connection can be established to `(host, port)` within `timeout` seconds. When `returntuple` is `True`, the function returns `(is_open, message)`, otherwise only the boolean is returned.
- **Notes:** Uses `socket.create_connection` and first tries a lightweight `ping` for reachability.

---

### ping_list(hosts: list[str], timeout: int = 2, count: int = 1) -> dict[str, bool]

- **Description:** Ping multiple hosts and return a mapping of host -> reachability (boolean).

---

### free_port_scanner(host: str, start_port: int, end_port: int, timeout: float = 1.0, show_progress: bool = False) -> list[int]

- **Description:** Scan a port range and return a list of ports considered free by this module's heuristic (note: the implementation uses `is_port_open` and collects ports that are `True`/free according to its logic).
- **Caveat:** Network, OS permission, and firewall rules can affect results. For accurate scanning consider platform-specific, privileged tools (e.g., `nmap`).

---

### scan_ports_list(host: str, ports: list[int], timeout: float = 1.0) -> dict[int, bool]

- **Description:** Scan an explicit list of ports and return a dictionary mapping port -> open status (boolean).

---

## Internal helpers and validators

### _tuple_is_port_open(host: str, port: int, timeout: float = 1.0) -> tuple[bool, str]

- **Description:** Internal helper used by `is_port_open` that returns `(is_open, message)`. It performs validation of the host and port and returns a descriptive message suitable for callers requesting a tuple result (via `returntuple=True`). Not intended for public use but useful for debugging or advanced callers.

### is_ip_valid(ip: str) -> bool

- **Description:** Validate whether a string is a valid IPv4 address. Returns `True` if the string contains exactly four numeric octets in the range 0–255.

### is_hostname_valid(hostname: str) -> bool

- **Description:** Validate hostname format according to common rules: total length up to 255 characters, labels separated by `.`, each label 1–63 characters, no leading or trailing hyphens, and only letters, digits, hyphens or dots allowed. Returns `True` for valid hostnames.

### is_port_valid(port: int) -> bool

- **Description:** Validate whether an integer is a valid TCP/UDP port number (0–65535). Returns `True` for valid ports.

---

## Examples

```python
from common.network import get_local_ip, get_public_ip, is_port_open

print(get_local_ip())
print(get_public_ip())
print(is_port_open('localhost', 22))  # True if SSH is listening locally
```

---

## Notes

- Because `ping` and external endpoints may behave differently across networks and platforms, these helpers are best used for lightweight checks and scripts rather than security-sensitive scans.
- Consider adding retries, exponential backoff, or configurable endpoints for more robust checks.
