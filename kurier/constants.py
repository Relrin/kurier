

NO_GAP = 0
DEFAULT_GAP = 5
DEFAULT_VERTICAL_GAP = 5
DEFAULT_HORIZONTAL_GAP = 5

DEFAULT_MESSAGE_PROPERTIES = (
    "content_type",
    "content_encoding",
    "priority",
    "correlation_id",
    "delivery_mode",
    "reply_to",
    "expiration",
    "message_id",
    "timestamp",
    "type",
    "user_id",
    "app_id",
    "cluster_id"
)

WRONG_JSON_UNICODE_SYMBOLS = [
    ("\u2028", "\\u2028"),
    ("\u2029", "\\u2029"),
]

AMQP_RESPONSE_RECEIVED_TOPIC = "AmqpResponseReceived"
