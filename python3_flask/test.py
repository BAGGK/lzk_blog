class BaseFormat(object):

    def __init__(self, temp_list):
        self.temp_list = [1, 2, 3]
        self.len = len(self.temp_list)

    def __next__(self):
        if self.len != 0:
            self.len -= 1
            return 1
        else:
            raise StopIteration

    def __iter__(self):
        return self


temp = BaseFormat(1)
for i in temp:
    print(i)