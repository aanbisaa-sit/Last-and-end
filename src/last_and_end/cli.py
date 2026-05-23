import argparse
from pathlib import Path
from .config_loader import load_config
from .render import render_summary
from .runner import run_checks
from .summary import summarize_results

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="last-and-end")
    parser.add_argument("--config", type=Path, default=Path("config.example.toml"))
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    print(render_summary(summarize_results(run_checks(config))))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
