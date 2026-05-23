# Changelog

All notable changes to `last-and-end` are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] — 2026-05-23

### Added
- `last-and-end` CLI entry-point with `--config` and `--version` flags.
- `config_loader.load_config`: parse TOML config → immutable `TrackerConfig`.
- `checker.check_endpoint`: HTTP-GET probe with timeout + retry support.
- `runner.run_checks(config)`: bulk-probe all endpoints from a `TrackerConfig`.
- `runner.run_endpoint_list(...)`: ad-hoc probe without full config object.
- `summary.summarize_results(...)`: tally healthy / degraded / down / unknown.
- `render.render_summary(...)`: human-readable status lines.
- `status.ServiceStatus`: StrEnum (`healthy`, `degraded`, `down`, `unknown`).
- `classifier.classify_result`: HTTP-code + error → `ServiceStatus`.
- `health_score`: relative health scoring between runs.
- `notifications`: `NotificationAdapter` protocol + `NoOpAdapter` stub.
- `trends`: health-score delta tracking over time.
- `serialize`: `result_to_dict` / `result_from_dict` JSON helpers.
- `availability_ratio`: compute uptime fraction from a result list.

### Fixed
- `config_loader`: guard against missing `name` / `url` / `expected_status`
  fields in endpoint entries (now defaults to `"unnamed"`, `""`, `200`).
- Negative `timeout_seconds` or `retries` now raise `ValueError` upfront
  instead of silently passing garbage to `urllib`.
- `config_loader`: malformed TOML surfaces as `ConfigurationError` instead
  of a raw `tomllib.TOMLDecodeError`.

### Docs
- Expanded `README.md` with install instructions, quick-start, and
  configuration reference.
- Expanded `config.example.toml` with inline comments and 5 endpoint patterns.
