class TagIter(object):

    def __init__(self, tag_list):
        self.tag_list = tag_list
        self.max_count = len(tag_list)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.max_count:
            raise StopIteration

        self.index += 1

        return {'tag_name': self.tag_list[self.index - 1].name,
                'tag_id': self.tag_list[self.index - 1].id
                }
