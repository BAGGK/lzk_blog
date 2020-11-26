# coding: utf-8
from liweb import View
from flask import request
from setting import app
from .model import Posts
import time
import flask
import uuid

from werkzeug.datastructures import FileStorage


class FileUpload(View):
    """/file_upload"""

    methods = ["POST"]

    @staticmethod
    def post():
        net_fd = request.files['file_name']  # type: FileStorage
        file_save_name = uuid.uuid4().hex
        save_path = app.root_path + '/posts/' + str(file_save_name)
        net_fd.save(save_path)
        net_fd.close()

        tags_list = ['python']
        fd = open(save_path)

        Posts.push(fd, tags_list)
        return "ok", 200


class PostsHeadView(View):
    """/posts_head"""

    @staticmethod
    def get():
        db_list = Posts.get_recent_posts()
        posts_list = []
        for each_item in db_list:  # type: PostHead
            item = PostsHeadView.parse_data_to_json(each_item)
            posts_list.append(item)

        ret_val = {
            'current_page': 0,
            'posts': posts_list
        }
        return flask.json.dumps(ret_val)

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
            'tags': [{
                'tag_url': 'https://www.baidu.com',
                'tag_name': 'python'
            }]
        }


class PostContentView(View):
    """/post_content"""

    methods = ['GET']

    @staticmethod
    def get():
        posts_uuid = request.args.get('posts_id')
        if posts_uuid:
            return Posts.get_html(posts_uuid)
        return '400'
