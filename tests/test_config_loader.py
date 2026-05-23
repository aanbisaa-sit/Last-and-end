from last_and_end.config_loader import load_config


def test_load_config_from_toml(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text('timeout_seconds = 3
[[endpoints]]
name = "api"
url = "https://example.com"
')
    config = load_config(path)
    assert config.timeout_seconds == 3
    assert config.endpoints[0].name == "api"
