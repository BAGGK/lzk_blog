from .model import Tag

"""
    对外界来看：(t_id, name ,posts_set）
"""


class TagContext(object):

    def __init__(self, t_id, name, posts_set=None):
        for k, v in locals().items():
            if k == 'self':
                continue
            elif v is not None:
                self.__setattr__(k, v)

    def __getattr__(self, item):
        if item == 'posts_set':
            self.posts_set = []
            return self.posts_set

        if item == 't_id':
            self.t_id = 0
            return self.t_id

        if item == 'name':
            self.name = 'undo'
            return self.name

        raise AttributeError("AttributeError: '%s' object has no attribute '%s"
                             % (self.__class__.__name__, item))


class DBAdapterTag(TagContext):

    def __init__(self, tag_db):
        tag_db: Tag
        super(DBAdapterTag, self).__init__(name=tag_db.name, t_id=tag_db.tag_id, posts_set=None)


class IDAdapterTag(TagContext):

    def __init__(self, t_id):
        super(IDAdapterTag, self).__init__(t_id, None, None)
