"""
tests/test_config_loader.py — edge cases + existing tests

Covers:
- defaults applied when fields are missing
- ConfigurationError raised when config file absent
- warning_stubs inline for hermetic testing
"""
import tomllib
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from last_and_end.config_loader import load_config
from last_and_end.errors import ConfigurationError


@pytest.fixture()
def tmp_toml(tmp_path: Path) -> Path:
    def _write(content: str) -> Path:
        p = tmp_path / "mock.toml"
        p.write_text(textwrap.dedent(content), encoding="utf-8")
        return p
    return _write


# ── helpers ──────────────────────────────────────────────────────────────────

def _endpoint(config, index: int = 0):
    return config.endpoints[index]


# ── happy-path defaults ──────────────────────────────────────────────────────

def test_minimal_config_applies_defaults(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "home"
    url  = "https://example.com"
    """)
    cfg = load_config(p)
    assert cfg.timeout_seconds == 5.0
    assert cfg.retries == 0
    assert len(cfg.endpoints) == 1
    assert _endpoint(cfg).name == "home"
    assert _endpoint(cfg).expected_status == 200


def test_missing_name_gets_placeholder(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    url  = "https://example.com"
    """)
    cfg = load_config(p)
    assert _endpoint(cfg).name == "unnamed"


def test_missing_url_gets_empty_string(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "no-url"
    """)
    cfg = load_config(p)
    assert _endpoint(cfg).url == ""


def test_missing_expected_status_defaults_to_200(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "api"
    url  = "https://api.example.com"
    """)
    cfg = load_config(p)
    assert _endpoint(cfg).expected_status == 200


def test_custom_timeout_and_retries(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "svc"
    url  = "https://svc.example.com"

    timeout_seconds = 10.0
    retries = 3
    """)
    cfg = load_config(p)
    assert cfg.timeout_seconds == 10.0
    assert cfg.retries == 3


def test_returns_empty_tuple_when_no_endpoints(tmp_toml):
    p = tmp_toml("""
    timeout_seconds = 7.0
    """)
    cfg = load_config(p)
    assert cfg.endpoints == ()


# ── error paths ───────────────────────────────────────────────────────────────

def test_missing_file_raises_configuration_error(tmp_path: Path):
    with pytest.raises(ConfigurationError, match="not found"):
        load_config(tmp_path / "ghost.toml")


def test_malformed_toml_raises(tmp_toml):
    p = tmp_toml("this is [[not valid]] toml {{{")
    with pytest.raises(Exception):
        load_config(p)


def test_preserves_order_of_endpoints(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]  name = "a"  url = "https://a"
    [[endpoints]]  name = "b"  url = "https://b"
    [[endpoints]]  name = "c"  url = "https://c"
    """)
    cfg = load_config(p)
    assert [e.name for e in cfg.endpoints] == ["a", "b", "c"]



# ── input validation ───────────────────────────────────────────────────────────

def test_negative_timeout_raises_value_error(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "svc"
    url  = "https://svc.example.com"

    timeout_seconds = -1.0
    """)
    with pytest.raises(ValueError, match="timeout_seconds"):
        load_config(p)


def test_negative_retries_raises_value_error(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "svc"
    url  = "https://svc.example.com"

    retries = -3
    """)
    with pytest.raises(ValueError, match="retries"):
        load_config(p)


def test_zero_timeout_is_allowed(tmp_toml):
    p = tmp_toml("""
    [[endpoints]]
    name = "svc"
    url  = "https://svc.example.com"

    timeout_seconds = 0.0
    """)
    cfg = load_config(p)
    assert cfg.timeout_seconds == 0.0


def test_malformed_toml_raises_configuration_error(tmp_toml):
    p = tmp_toml("this is [[not valid toml {{{")
    with pytest.raises(ConfigurationError, match="Invalid TOML"):
        load_config(p)
