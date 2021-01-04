from time import strftime


class FitnessContext(object):
    def __init__(self, weight, date=None):
        self.weight = weight
        self.date = date if date else strftime('%Y-%m-%d')
