from .input import BaseInput
from .model import Tag, Posts

"""
    对外界来看：(id, name ,posts_set）
"""


class TagContext(object):

    def __init__(self, name, t_id):
        if t_id:
            self.id = t_id

        self.name = name

    def __getattr__(self, item):
        if item == 'posts_set':
            self.posts_set = []
            return self.posts_set

        if item == 'id':
            self.id = 0
            return self.id
        raise AttributeError("AttributeError: '%s' object has no attribute '%s"
                             % (self.__class__.__name__, item))


class DBAdapterTag(TagContext):

    def __init__(self, tag_db):
        tag_db: Tag
        super(DBAdapterTag, self).__init__(name=tag_db.name, t_id=tag_db.tag_id)
