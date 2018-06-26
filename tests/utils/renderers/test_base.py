import pytest


from kurier.utils.renderers.base import BaseRenderer


def test_base_renderer_raises_type_error_for_not_implemented_render_method():
    with pytest.raises(TypeError):
        instance = BaseRenderer()
        instance.Render('wtf')
