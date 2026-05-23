from last_and_end.cli import build_parser


def test_parser_accepts_config_argument():
parser = build_parser()
args = parser.parse_args(["--config", "custom.toml"])
assert str(args.config) == "custom.toml"
