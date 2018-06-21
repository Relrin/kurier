

class BaseAmqpException(Exception):
    pass


class AmqpInvalidUrl(BaseAmqpException):
    pass


class AmqpInvalidExchange(BaseAmqpException):
    pass


class AmqpUnroutableError(BaseAmqpException):
    pass


class AmqpRequestCancelled(BaseAmqpException):
    pass
