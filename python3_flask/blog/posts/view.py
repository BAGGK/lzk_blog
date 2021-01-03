from blog.liweb import View
from flask import request, json
import time
from .posts_context import FileStorageAdapterPosts
from werkzeug.datastructures import FileStorage
from .model import TagIter, Tag


class FileUpload(View):
    """/file_upload/"""

    methods = ["GET", "POST"]

    @staticmethod
    def get():
        tag_list = Tag.get_list(0)
        ret_val = []
        for tag_name in TagIter(tag_list):
            ret_val.append(tag_name)
        return json.dumps(ret_val), 200

    @staticmethod
    def post():
        f_list = request.files.getlist('file_name')
        tags = request.form.getlist('posts_tags')
        tags = list(map(int, tags))

        for file_instance in f_list:
            file_instance: FileStorage
            posts_context = FileStorageAdapterPosts(file_instance, *tags)
            posts_context.save()

        return "upload file success", 200


class PostsHeadView(View):
    """/posts_head/"""

    @staticmethod
    def get():
        # limit = request.form.get('limit', None)
        # tags_list = request.form.get('tags', None)
        #
        # db_list = Posts.get_recent_posts(limit_num=limit)
        # posts_list = []
        # for each_item in db_list:  # type: PostHead
        #     item = PostsHeadView.parse_data_to_json(each_item)
        #     posts_list.append(item)
        #
        # ret_val = {
        #     'current_page': 0,
        #     'posts': posts_list
        # }
        # return flask.json.dumps(ret_val)
        pass

    @staticmethod
    def parse_data_to_json(posts):
        """
        :type posts: PostHead
        """
        posts_time = time.strftime('%a, %b %d, %Y', time.localtime(posts.posts_ctime))

        return {
            'url': str(posts.posts_uuid),
            'title': posts.posts_title,
            'content': posts.posts_head,
            'date': posts_time,
            'tags': json.loads(posts.posts_tags)
        }


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
