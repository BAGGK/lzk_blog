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
        if hasattr(self, 'posts_id') and self.posts_id:
            self.query_ins = self.query_ins.filter_by(posts_id=self.posts_id)

    def __limit(self):
        pass


class PostsQueryAll(PostsQuery):
    def __init__(self, limit=30):
        super(PostsQueryAll, self).__init__()
        self.limit = limit


class PostsQueryById(PostsQuery):
    def __init__(self, posts_id):
        super(PostsQueryById, self).__init__()
        self.posts_id = posts_id


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
        if hasattr(self, 'tag_id') and self.tag_id:
            self.query_ins = self.query_ins.filter_by(tag_id=self.tag_id)

    def __order_limit(self):

        if hasattr(self, 'limit') and self.limit != 0:
            self.query_ins.limit(self.limit)


class PostsQueryByTagId(TagQuery):
    def __init__(self, tag_id):
        super(PostsQueryByTagId, self).__init__()
        self.tag_id = tag_id

    def all(self):
        tag: Tag = super(PostsQueryByTagId, self).all()[0]
        return tag.posts_set


class TagQueryAll(TagQuery):

    def __init__(self):
        super(TagQueryAll, self).__init__()
        self.limit = 0
