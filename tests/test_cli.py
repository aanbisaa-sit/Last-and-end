"""
tests/test_cli.py

Covers:
- --version exits with code 0 and prints version string
- --config accepts a custom path and runs without error
- Missing config file produces a non-zero exit code / error
"""
import textwrap

import pytest

from last_and_end import __version__


# ── --version ────────────────────────────────────────────────────────────────

def test_version_flag(capsys):
    """build_parser --version should print the package version and exit(0)."""
    from last_and_end.cli import build_parser

    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--version"])
    assert exc.value.code == 0  # argparse returns 0 for --version


def test_version_flag_prints_version_and_exits_zero(capsys):
    from last_and_end.cli import main

    # --version should exit cleanly after printing the version string
    with pytest.raises(SystemExit) as exc:
        main(["--version", "--config", "unused-toml"])
    captured = capsys.readouterr()
    assert exc.value.code == 0
    assert __version__ in captured.out


# ── --config ─────────────────────────────────────────────────────────────────

def test_missing_config_exits_nonzero(tmp_path):
    """Custom config path → ConfigurationError → sys.exit(2)."""
    import sys
    from unittest.mock import patch

    from last_and_end.cli import main

    with pytest.raises(SystemExit) as exc, \
         patch("pathlib.Path.exists", return_value=False):
        main(["--config", str(tmp_path / "ghost.toml")])
    assert exc.value.code == 2


def test_main_with_valid_config(tmp_path, capsys):
    """main() with a valid config runs and returns 0."""
    p = tmp_path / "ok.toml"
    p.write_text(textwrap.dedent("""
    [[endpoints]]
    name = "health"
    url  = "http://localhost:9999/health"
    expected_status = 503
    """), encoding="utf-8")

    from last_and_end.cli import main
    # No network is reachable at 9999; runner handles errors.
    code = main(["--config", str(p)])
    assert code == 0
