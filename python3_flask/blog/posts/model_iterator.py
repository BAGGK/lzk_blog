import time
import markdown
from .posts_context import PostsContext
from .tag_context import TagContext


class BaseIter(object):

    def __init__(self, ctx_list):
        self.ctx_list = ctx_list
        self.max_count = len(ctx_list)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == self.max_count:
            raise StopIteration
        self.index += 1

        return self.data_form(self.ctx_list[self.index - 1])

    @staticmethod
    def data_form(ctx_item):
        raise NotImplementedError


class TagIter(BaseIter):
    @staticmethod
    def data_form(tag_item):
        obj = {
            'tag_name': tag_item.name,
            'tag_id': tag_item.t_id
        }
        return obj


class PostsHeadsHtmlIter(BaseIter):
    @staticmethod
    def data_form(posts_item):
        posts_item: PostsContext

        posts_time = time.strftime('%a, %b %d, %Y', time.localtime(posts_item.last_modify_time / 1000))
        tags = []
        for each_tag in posts_item.tags:
            each_tag: TagContext
            json_tag = {
                'tag_url': each_tag.t_id,
                'tag_name': each_tag.name
            }
            tags.append(json_tag)
        intro_html = markdown.markdown(posts_item.introduction,
                                    extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        obj = {
            'url': posts_item.posts_id,
            'title': posts_item.title,
            'content': intro_html,
            'date': posts_time,
            'tags': tags
        }
        return obj
