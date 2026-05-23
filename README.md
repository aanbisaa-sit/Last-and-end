# Last and End

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: v0.1.0](https://img.shields.io/badge/status-0.1.0-green.svg)](https://github.com/aanbisaa-sit/Last-and-end/releases)

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
- **Transitions** — diff a current run against the previous result to get
  per-status movement counts (e.g. `healthy→down: 2`).
- **Serialisable** — `result_to_dict` / `result_from_dict` round-trip via JSON.
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

## Advanced topics

### Running with Make

```bash
make install   # install deps + dev tools
make test      # run the full test suite
make lint      # ruff lint
make typecheck # mypy
make run       # quick-endpoint probe
make all       # format + lint + typecheck + test
```

### Detecting state transitions

Pass the *previous* summary to `summarize_results` to get a transition map:

```python
from last_and_end.summary import summarize_results

prev = {ServiceStatus.HEALTHY: 3, ServiceStatus.DOWN: 0, ...}
transitions = summarize_results(current_results, previous=prev)
# {"healthy->healthy": 2, "healthy->degraded": 1, ...}
```

### Using the serializer

```python
from last_and_end.serialize import result_to_dict, result_from_dict
import json

d = result_to_dict(check_result)
blob = json.dumps(d)          # safe to store / send
restored = result_from_dict(json.loads(blob))
assert restored == check_result
```

### Exception hierarchy

| Exception                  | Meaning                          |
|----------------------------|----------------------------------|
| `TrackerError`             | base class for all package errors|
| `ConfigurationError`       | bad or missing config file       |
| `CheckError`               | checker invariant violated       |
| `TimeoutError`             | single attempt exceeded deadline |
| `RetryExhaustedError`      | all retries consumed             |

Catch `RetryExhaustedError` when you need to distinguish "temporary glitch"
from "permanent down":

```python
from last_and_end.checker import check_endpoint
from last_and_end.errors import RetryExhaustedError

try:
    check_endpoint(ep, timeout_seconds=3, retries=2)
except RetryExhaustedError as exc:
    print(f"Gave up after {exc.attempts} attempts — {exc.last_error}")
```

## Development

```bash
# Install dev tools
make install

# Run tests
make test

# Type-check
make typecheck

# Fix lint issues
make lint-fix

# Pre-commit hooks (run once)
pre-commit install
```

## License

MIT — see [LICENSE](LICENSE).
