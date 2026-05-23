from last_and_end.fixtures import sample_result


def test_sample_result_uses_default_endpoint():
result = sample_result()
assert result.endpoint.name == "homepage"
assert result.status_code == 200
