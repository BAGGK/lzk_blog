from blog.global_class.base_input import BaseInput


class PostsStorageInput(object):
    def __init__(self, posts_st, *save_db):
        self.data = posts_st
        self.save_db = save_db

    def save(self):
        try:
            for each_db in self.save_db:
                each_db(self.data).save()
        except Exception as e:
            print('Input error', e)


class FileInput(BaseInput):

    def save(self):
        pass


class RedisInput(BaseInput):

    def save(self):
        pass


class DbInput(BaseInput):

    def save(self):
        pass
