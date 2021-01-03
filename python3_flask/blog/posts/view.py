from blog.liweb import View
from flask import request, json
from blog import app
from .model import Posts, PostsTag
import time
from werkzeug.datastructures import FileStorage


class FileUpload(View):
    """/file_upload/"""

    methods = ["POST"]

    @staticmethod
    def post():

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
