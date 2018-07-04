

class IStateRestorable(object):

    def InitFromState(self, **state):
        raise NotImplementedError("InitFromState(**state) method must be implemented.")
