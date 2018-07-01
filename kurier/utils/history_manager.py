from typing import Dict


class State(object):

    def __init__(self, *args, **kwargs):
        self._connection_url = kwargs.pop("connection_url", "")
        self._request_exchange = kwargs.pop("request_exchange", "")
        self._request_routing_key = kwargs.pop("request_routing_key", "")
        self._response_queue = kwargs.pop("response_queue", "")
        self._response_exchange = kwargs.pop("response_exchange", "")
        self._response_routing_key = kwargs.pop("response_routing_key", "")
        self._properties = kwargs.pop("properties", {})
        self._headers = kwargs.pop("headers", {})
        self._body = kwargs.pop("body", "")

    def GetDump(self):
        return {
            "connection_url": self._connection_url,
            "request_exchange": self._request_exchange,
            "request_routing_key": self._request_routing_key,
            "response_queue": self._response_queue,
            "response_exchange": self._response_exchange,
            "response_routing_key": self._response_routing_key,
            "properties": self._properties,
            "headers": self._headers,
            "body": self._body,
        }


class HistoryManager(object):
    MAX_STATES = 30

    def __init__(self, *args, **kwargs):
        self._data = []

    @property
    def SavedStates(self):
        return len(self._data)

    def AddState(self, state_data: Dict):
        if self.SavedStates >= self.MAX_STATES:
            self.RemoveOldState()

        state = State(**state_data)
        self._data.insert(0, state)

    def GetState(self, index):
        if index > self.SavedStates:
            raise IndexError("List index out of range.")

        return self._data[index].GetDump()

    def RemoveOldState(self):
        if self._data:
            self._data.pop()
