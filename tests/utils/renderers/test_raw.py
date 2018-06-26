import pytest

from kurier.utils.renderers.raw import RawRenderer


@pytest.mark.parametrize("data,expected", [
    (None, True),
    ("", True),
    ({"key": "value"}, True),
    ([1, 2, 3], True),
    ("not_mimetype", True),
    ("application/json", True),
])
def test_raw_renderer_returns_true_for_any_mimetype(data, expected):
    assert RawRenderer.IsValidMimetype(data) is expected


@pytest.mark.parametrize("data,expected", [
    ("text", "text"),
    ({"key": "value"}, {"key": "value"}),
    (None, None),
])
def test_raw_renderer_returns_data_as_is(data, expected):
    instance = RawRenderer()
    assert instance.Render(data) == expected
