from abc import abstractmethod


class BaseRenderer(object):

    @staticmethod
    @abstractmethod
    def IsValidMimetype(value):
        pass

    @abstractmethod
    def Render(self, data):
        pass
