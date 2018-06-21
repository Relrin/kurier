from threading import Thread as BaseThread, Event


class Thread(BaseThread):

    def __init__(self, event=None, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.event = event

    def IsEventSet(self):
        return isinstance(self.event, Event) and self.event.is_set()
