from blog.liweb import View
from flask import request, json
import markdown
from .posts_context import FileStorageAdapter
from .query import TagQueryAll, PostsQueryAll, PostsQueryById
from .model_interface import ModelInterface
from .model_iterator import TagIter, PostsHeadsHtmlIter
from .validator import IntegerField, FileField


class FileUpload(View):
    """/file_upload/"""

    methods = ["GET", "POST"]

    @staticmethod
    def get():
        tag_list = ModelInterface.output(TagQueryAll())

        ret_val = []
        for tag_name in TagIter(tag_list):
            ret_val.append(tag_name)
        return json.dumps(ret_val), 200

    @classmethod
    def post(cls):
        f_list = FileField('file_name', is_list=True)
        tags = IntegerField('posts_tags', is_list=True)
        last_modify_time = IntegerField('last_modify_time', is_list=True)

        for each_var in (f_list, tags, last_modify_time):
            if each_var is False:
                return 'Please input correct data', 400

        for each_file, modify_time in zip(f_list, last_modify_time):
            temp_var = FileStorageAdapter(each_file, tags, modify_time)
            ModelInterface.input(temp_var)

        return "upload file success", 200


class PostsHeadView(View):
    """/posts_head/"""

    @staticmethod
    def get():
        limit = IntegerField('limit')
        tags_list = IntegerField('tags', is_list=True)

        if limit is False or tags_list is False:
            return '参数错误', 400

        posts_ctx_list = ModelInterface.output(PostsQueryAll(limit))

        posts_list = []
        for each_item in PostsHeadsHtmlIter(posts_ctx_list):
            posts_list.append(each_item)

        ret_val = {
            'current_page': 0,
            'posts': posts_list
        }
        return json.dumps(ret_val)


class PostContentView(View):
    """/posts_content/"""

    methods = ['GET']

    @staticmethod
    def get():
        posts_id = IntegerField('posts_id')

        if posts_id is False:
            return '请输入正确的posts_id', 400

        posts_ctx = ModelInterface.output(PostsQueryById(posts_id))[0]
        ret_var = markdown.markdown(posts_ctx.content,
                                    extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        ret_var = '<link rel="stylesheet" href="blog.css">' + ret_var
        return ret_var
