

class BaseConverter(object):

    def __init__(self, *args, **kwargs):
        self.options = kwargs

    def to_internal_value(self, value):
        raise NotImplementedError('`to_representation()` method must be implemented.')


class StringConverter(BaseConverter):

    def to_internal_value(self, value):
        return str(value)


class IntegerConverter(BaseConverter):

    def to_internal_value(self, value):
        default = self.options.get('default', None)

        try:
            result = int(value)
        except (ValueError, TypeError):
            result = default

        return result
