from abc import abstractmethod, ABCMeta


class BaseRenderer(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def IsValidMimetype(value):
        pass

    @abstractmethod
    def Render(self, data):
        pass
