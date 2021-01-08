from blog.liweb import View
from flask import request, json
import time
from .posts_context import FileStorageAdapter
from .query import TagQueryAll, PostsQueryAll
from .model_interface import ModelInterface
from .model_iterator import TagIter, PostsHeadsHtmlIter
from .validator import IntegerField


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
        f_list = request.files.getlist('file_name')
        tags = request.form.getlist('posts_tags')
        tags = list(map(int, tags))
        last_modify_time = request.form.getlist('last_modify_time')
        last_modify_time = list(map(int, last_modify_time))

        if not cls.post_validate(f_list, tags, last_modify_time):
            return 'Please input correct data', 400

        for each_file, modify_time in zip(f_list, last_modify_time):
            temp_var = FileStorageAdapter(each_file, tags, modify_time)
            ModelInterface.input(temp_var)

        return "upload file success", 200

    @staticmethod
    def post_validate(f_list, tags, last_modify_time):

        if len(f_list) != len(last_modify_time):
            return False

        for each_data in tags:
            if each_data <= 0:
                return False

        return True


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
        # posts_uuid = request.args.get('posts_id')
        # if posts_uuid:
        #     return Posts.get_html(posts_uuid)
        # return '400'
        pass
