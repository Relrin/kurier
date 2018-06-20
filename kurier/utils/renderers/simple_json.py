import json

from kurier.constants import WRONG_JSON_UNICODE_SYMBOLS
from kurier.utils.renderers.base import BaseRenderer


class JsonRenderer(BaseRenderer):

    @staticmethod
    def IsValidMimetype(value):
        return isinstance(value, str) and value.strip() in ['application/json', ]

    def Render(self, data):
        try:
            response = json.loads(data)
            response = self.BeautifyJSON(response)
        except (TypeError, json.JSONDecodeError):
            response = data

        return response

    def ReplaceSymbols(self, data, replacements):
        for wrong_symbol, expected in replacements:
            data = data.replace(wrong_symbol, expected)

        return data

    def BeautifyJSON(self, json_data):
        raw_data = json.dumps(json_data, sort_keys=False, indent=4)
        raw_data = self.ReplaceSymbols(raw_data, WRONG_JSON_UNICODE_SYMBOLS)
        return raw_data
