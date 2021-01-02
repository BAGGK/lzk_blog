from blog.liweb import View
from flask import request, json
from blog import app
from .model import Posts, PostsTag
import time
import flask
import uuid
import os
import wtforms
from werkzeug.datastructures import FileStorage


class FileContext(object):

    def __init__(self, up_name):
        self.fs_list = request.files.getlist(up_name)
        self.tags = request.form.get('posts_tags', None)

    def save(self):
        each_file: FileStorage

        save_path = app.root_path + '/posts/save_file/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        file_save_name = uuid.uuid4().hex
        save_file = save_path + str(file_save_name)

        for each_file in self.fs_list:
            each_file.save(save_file)



class FileUpload(View):
    """/file_upload/"""

    methods = ["POST", 'GET']

    @staticmethod
    def post():
        file_handle = FileContext(up_name='file_name')
        file_handle.save()
        return "upload file success", 200
        # net_fd = request.files.get('file_name', None)  # type: FileStorage
        # tags = request.form.get('tags', None)
        # if net_fd is None:
        #     return 'You must input a file', 400
        #
        # if tags is None:
        #     tags = ''
        #
        # tags_list = json.loads(tags)
        # # 保存文件到本地
        # save_file = FileUpload.__save_file(net_fd)
        # net_fd.close()
        #
        # # 解析文件，并且存入数据库
        # fd = open(save_file)
        # Posts.push(fd, tags_list)
        # for item_tag in tags_list:
        #     PostsTag(posts_uuid=os.path.basename(fd.name), posts_tag=item_tag).push()
        # return "upload file success", 200

    # @staticmethod
    # def __save_file(net_fd):
    #     save_path = app.root_path + '/save_file/'
    #     if not os.path.exists(save_path):
    #         os.mkdir(save_path)
    #     file_save_name = uuid.uuid4().hex
    #     save_file = save_path + str(file_save_name)
    #     net_fd.save(save_file)
    #     return save_file


class PostsHeadView(View):
    """/posts_head/"""

    @staticmethod
    def get():
        limit = request.form.get('limit', None)
        tags_list = request.form.get('tags', None)

        db_list = Posts.get_recent_posts(limit_num=limit)
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
            'tags': json.loads(posts.posts_tags)
        }


class PostContentView(View):
    """/posts_content/"""

    methods = ['GET']

    @staticmethod
    def get():
        posts_uuid = request.args.get('posts_id')
        if posts_uuid:
            return Posts.get_html(posts_uuid)
        return '400'


class IndexView(View):
    """
    /index
    """
    methods = ['GET']

    @staticmethod
    def get():
        return 'index hello'
