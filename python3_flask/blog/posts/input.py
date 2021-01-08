from blog.global_class import BaseInput
from blog import db
from .model import Posts, PostsTag
from .posts_context import PostsContext
from .tag_context import TagContext


class PostsInput(BaseInput):

    def save(self):
        """
            这里是创建posts的时候，那 tags 就一定有。问题是如何确保是有效的。
        """
        posts_context: PostsContext = self.data

        content = posts_context.content
        filename = posts_context.filename
        last_modify_time = posts_context.last_modify_time

        temp_var = Posts(content=content, filename=filename, last_modify_time=last_modify_time)
        session: db.Session = db.session
        session.add(temp_var)
        session.flush()

        posts_tag_list = []
        for each_tag in posts_context.tags:
            each_tag: TagContext
            posts_tag_list.append(PostsTag(posts_id=temp_var.posts_id, tag_id=each_tag.t_id))

        session.add_all(posts_tag_list)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print('commit error', e)


class TagInput(BaseInput):

    def save(self):
        pass


class InputFactor(object):

    def __new__(cls, item):
        if isinstance(item, PostsContext):
            return PostsInput
        elif isinstance(item, TagContext):
            return TagInput
