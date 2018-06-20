from kurier.utils.renderers.base import BaseRenderer


class RawRenderer(BaseRenderer):

    @staticmethod
    def IsValidMimetype(_value):
        return True

    def Render(self, data):
        return data
