class BaseInput(object):
    def __init__(self, data):
        self.data = data

    def save(self):
        raise NotImplementedError
