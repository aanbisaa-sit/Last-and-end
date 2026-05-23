# Last and End

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: v0.1.0](https://img.shields.io/badge/status-0.1.0-green.svg)]

Last and End is a lightweight uptime and downtime tracker for personal sites,
small APIs, and lightweight services.

It turns simple endpoint health checks into readable status summaries — with
zero external dependencies beyond the Python standard library.

## Features

- **Zero dependencies** — only `urllib` and `tomllib` from the stdlib.
- **Immutable config** — frozen dataclasses, safe to share across threads.
- **Retry support** — configurable per-attempt timeout and retry count.
- **Structured results** — `CheckResult` objects with latency, status, and
  error annotations.
- **Extensible** — plug in your own notifier via the `NotificationAdapter`
  protocol (see `src/last_and_end/adapters.py`).

## Install

```bash
# From PyPI (when published)
pip install last-and-end

# Or from source
git clone https://github.com/aanbisaa-sit/Last-and-end.git
cd Last-and-end
pip install .
```

## Quick start

1. Copy the example config:

```bash
cp config.example.toml config.toml
```

2. Edit `config.toml` and set your own endpoints.

3. Run a single check:

```bash
python -m last_and_end --config config.toml
```

4. Run from the CLI entry-point:

```bash
last-and-end --config config.toml
```

## Config file

```toml
timeout_seconds = 5   # per-attempt socket timeout (seconds, >= 0)
retries = 0            # extra attempts after first failure (>= 0)

[[endpoints]]
name              = "homepage"
url               = "https://example.com"
expected_status   = 200
```

## Output

```
Availability: 100.00%  (2 / 2 healthy)
Healthy  : homepage, api
Degraded : -
Down     : -
```

## Status values

| Value      | Meaning                       |
|------------|-------------------------------|
| `healthy`  | status code == expected       |
| `degraded` | status code != expected       |
| `down`     | network error / unreachable   |
| `unknown`  | no checks have run            |

## Development

```bash
# Run tests
pytest tests/

# Type-check
mypy src/last_and_end/
```

## License

MIT — see [LICENSE](LICENSE).
