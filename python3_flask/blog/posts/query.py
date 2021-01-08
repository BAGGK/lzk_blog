__name__ = 'blog.posts.query'
from blog.global_class import BaseQuery
from blog import db
from .model import Tag, Posts


class PostsQuery(BaseQuery):

    def __init__(self):
        self.class_type = Posts
        self.query_ins = db.session.query(Posts)

    def all(self):
        self.__filter()
        self.__limit()

        return self.query_ins.all()

    def __filter(self):
        pass

    def __limit(self):
        pass


class PostsQueryAll(PostsQuery):
    def __init__(self, limit=30):
        super(PostsQueryAll, self).__init__()
        self.limit = limit


class TagQuery(BaseQuery):

    def __init__(self):
        self.class_type = Tag
        self.query_ins = db.session.query(self.class_type)

    def all(self):
        self.__filter()
        self.__order_limit()
        return self.query_ins.all()

    def __filter(self):
        if hasattr(self, 'name') and self.name:
            self.query_ins = self.query_ins.filter_by(name=self.name)

    def __order_limit(self):

        if hasattr(self, 'limit') and self.limit != 0:
            self.query_ins.limit(self.limit)


class TagQueryAll(TagQuery):

    def __init__(self):
        super(TagQueryAll, self).__init__()
        self.limit = 0
