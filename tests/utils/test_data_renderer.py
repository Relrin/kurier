import pytest

from kurier.utils.data_renderer import DataRenderer


@pytest.mark.parametrize("data,mimetype,expected", [
    ("text", "UNKNOWN", "text"),
])
def test_data_renderer_returns_data_as_is_for_unknown_mimetype(data, mimetype, expected):  # NOQA
    instance = DataRenderer()
    assert instance.Render(data, mimetype) == expected


@pytest.mark.parametrize("data,mimetype,expected", [
    ('{"key": "value"}', "application/json", '{\n    "key": "value"\n}'),
])
def test_data_renderer_returns_data_as_json_for_json_mimetype(data, mimetype, expected):  # NOQA
    instance = DataRenderer()
    assert instance.Render(data, mimetype) == expected
