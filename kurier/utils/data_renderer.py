from kurier.utils.renderers.raw import RawRenderer
from kurier.utils.renderers.simple_json import JsonRenderer


class DataRenderer(object):
    DEFAULT_RENDERERS = [JsonRenderer, ]

    def __init__(self, renderers=None, default_renderer=None, *args, **kwargs):
        self.default_renderer = default_renderer or RawRenderer
        self.renderers = renderers or self.DEFAULT_RENDERERS

    def Render(self, data, mimetype):
        renderer = self.GetRenderer(mimetype)
        return renderer.Render(data)

    def GetRenderer(self, mimetype):
        for renderer_cls in self.renderers:
            if renderer_cls.IsValidMimetype(mimetype):
                return renderer_cls()

        return self.default_renderer()
