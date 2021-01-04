class FitnessListIter(object):
    def __init__(self, fit_list):
        self.fit_list = fit_list
        self.max_count = len(fit_list)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.max_count:
            raise StopIteration
        self.index += 1
        return self.fit_list[self.index - 1].weight
