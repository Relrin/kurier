

class BaseAmqpException(Exception):
    default_detail = "Occurred an unexpected error."

    def __init__(self, detail=None):
        self.detail = detail if detail is not None else self.default_detail

    def __str__(self):
        return self.detail


class AmqpInvalidUrl(BaseAmqpException):
    default_detail = "The specified URL is invalid."


class AmqpInvalidExchange(BaseAmqpException):
    default_detail = "The specified exchange doesn't exist."


class AmqpUnroutableError(BaseAmqpException):
    default_detail = "The message can't be delivered."


class AmqpRequestCancelled(BaseAmqpException):
    default_detail = "The request was cancelled."
