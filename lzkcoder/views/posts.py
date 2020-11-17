# coding: utf-8
from liweb import View
from flask import request
from config import app
from model import PostHead
import time
import flask
import werkzeug.datastructures


class FileUpload(View):
    """/file_upload"""

    methods = ["GET", "POST"]

    @staticmethod
    def get():
        return 'hello'

    @staticmethod
    def post():
        f = request.files['file_name']
        f.save(app.root_path + '/posts/' + f.filename)
        print app.root_path + '/posts/' + f.filename
        return "ok", 200


#
# {
#     'url': "https://themes.gohugo.io//theme/anatole/post/markdown-syntax/",
#     'title': 'python 语法',
#     'content': '这遍文章主要是介绍 python 的基础语法。比如 列表 字典 元组 集合',
#     'date': 'Mon, Mar 11, 2019',
#     'tags': [{
#         'tag_url': 'https://themes.gohugo.io//theme/anatole/tags/markdown/',
#         'tag_name': 'markdown'
# }
class PostsHeadView(View):
    """/posts_head"""

    @staticmethod
    def get():
        db_list = PostHead.get_recent_data()
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
        post_time = time.strftime('%a, %b %d, %Y', time.localtime(posts.post_time))
        return {
            'url': posts.post_id,
            'title': posts.post_title,
            'content': posts.post_content,
            'date': post_time,
            'tags': [{
                'tag_url': 'https://www.baidu.com',
                'tag_name': 'python'
            }]
        }
