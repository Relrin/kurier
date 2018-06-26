import pytest

from kurier.utils.renderers.simple_json import JsonRenderer


@pytest.mark.parametrize("data,expected", [
    (None, False),
    ("", False),
    ({"key": "value"}, False),
    ([1, 2, 3], False),
    ("not_mimetype", False),
    ("application/json", True),
])
def test_json_renderer_returns_true_only_for_json_mimetype(data, expected):
    assert JsonRenderer.IsValidMimetype(data) is expected


@pytest.mark.parametrize("data,expected", [
    ('{"key": "value"}', '{\n    "key": "value"\n}'),
])
def test_json_renderer_returns_beautified_json(data, expected):
    instance = JsonRenderer()
    assert instance.Render(data) == expected


@pytest.mark.parametrize("data,expected", [
    ("null", "null"),
    ("not text: definitely", "not text: definitely")
])
def test_json_renderer_returns_invalid_data_as_is(data, expected):
    instance = JsonRenderer()
    assert instance.Render(data) == expected
