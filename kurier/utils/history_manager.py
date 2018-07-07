import json

from typing import Dict
from pathlib import Path


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
    HISTORY_FILENAME = "history.txt"
    HISTORY_FILE_OPTIONS = {
        "encoding": "utf-8",
        "newline": "\n"
    }

    def __init__(self, app_directory=None, *args, **kwargs):
        self._data = []
        self._app_directory = None
        self._history_filepath = None

        if isinstance(app_directory, str):
            self.app_directory = Path(app_directory)
            self.app_directory.mkdir(parents=True, exist_ok=True)

            self._history_filepath = self.app_directory.joinpath(self.HISTORY_FILENAME)
            self._history_filepath.touch(exist_ok=True)

            init_history_file = self._history_filepath.open(mode="rt+", **self.HISTORY_FILE_OPTIONS)  # NOQA
            self.ImportHistoryFromFile(init_history_file)

    @property
    def SavedStates(self):
        return len(self._data)

    def ImportHistoryFromFile(self, history_file):
        if history_file.closed:
            return

        if hasattr(history_file, 'seekable'):
            history_file.seek(0)

        with history_file:
            for state_dump in history_file.read().splitlines():
                try:
                    state_data = json.loads(state_dump)
                    self.AddState(state_data)
                except (TypeError, ValueError, json.JSONDecodeError):
                    pass

    def AddState(self, state_data: Dict):
        if self.SavedStates >= self.MAX_STATES:
            self.RemoveOldState()

        state = State(**state_data)
        self._data.insert(0, state)

        if self._history_filepath

    def GetState(self, index):
        if index > self.SavedStates:
            raise IndexError("List index out of range.")

        return self._data[index].GetDump()

    def RemoveOldState(self):
        if self._data:
            self._data.pop()
