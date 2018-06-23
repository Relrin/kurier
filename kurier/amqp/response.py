

class Response(object):

    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('body', '')
        self.properties = kwargs.pop('properties', {})
        self.headers = kwargs.pop('headers', {})
