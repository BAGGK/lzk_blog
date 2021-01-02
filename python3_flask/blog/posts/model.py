from blog import db
import os
import markdown
import json
from sqlalchemy.orm import relationship

"""
Posts 表 ｜ PostsTag 表

"""


class Posts(db.Model):
    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    posts_filename = db.Column(db.String(128), nullable=False)
    posts_path = db.Column(db.String(128))
    posts_file_create = db.Column(db.BigInteger)
    posts_uuid = db.Column(db.String(128))

    # def __init__(self, fd, posts_tags):
    #     """
    #
    #     :type fd: file
    #     """
    #     # 以下是实例传递参数
    #     self.fd = fd
    #     # end
    #     posts_title, posts_head, posts_ctime, posts_mtime = self.__parse_file_head()
    #     self.posts_uuid = os.path.basename(fd.name)
    #     self.posts_title = posts_title
    #     self.posts_head = posts_head
    #     self.posts_ctime = posts_ctime
    #     self.posts_mtime = posts_mtime
    #     self.posts_tags = json.dumps(posts_tags)
    #     # self.posts_filename = file_name
    #     self.posts_html = self.__md_to_html()
    #
    # def __md_to_html(self):
    #     self.fd.seek(0)
    #     md_unicode = self.fd.read()
    #
    #     return markdown.markdown(
    #         md_unicode,
    #         extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite']
    #     )
    #
    # def __parse_file_head(self):
    #     fd = self.fd
    #
    #     posts_title = fd.readline().lstrip('# ').strip()
    #     posts_head = fd.readline().strip()
    #     while posts_head == '':
    #         posts_head = fd.readline().strip()
    #     posts_ctime = os.path.getctime(fd.name)
    #     posts_mtime = os.path.getmtime(fd.name)
    #     return posts_title, posts_head, posts_ctime, posts_mtime
    #
    # # 以下是外部接口
    # @staticmethod
    # def get_recent_posts(limit_num=30, *tags):
    #     posts_query = Posts.make_condition(Posts.query, *tags)
    #     return posts_query.order_by(Posts.posts_ctime).limit(limit_num).all()
    #
    # @staticmethod
    # def make_condition(var_q, *tags):
    #     """
    #
    #     :type var_q: flask_sqlalchemy.BaseQuery
    #     """
    #     # 这个函数需要连表
    #     return var_q
    #
    # @staticmethod
    # def push(fd, tags):
    #     new_data = Posts(fd, tags)
    #     db.session.add(new_data)
    #     db.session.commit()
    #
    # @staticmethod
    # def pop(uuid):
    #     Posts.query.filter_by(uuid)
    #
    # @staticmethod
    # def get_html(uuid):
    #     ret_var = db.session.query(Posts.posts_html).filter(Posts.posts_uuid == uuid).first()  # type: Posts
    #
    #     ret_var = '<link rel="stylesheet" href="blog.css">' + ret_var.posts_html
    #     if ret_var:
    #         return ret_var
    #     else:
    #         return None


class PostsTag(db.Model):
    posts_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), primary_key=True)

    # def __init__(self, posts_tag, posts_uuid):
    #     self.posts_uuid = posts_uuid
    #     self.posts_tag = posts_tag
    #
    # def push(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # @staticmethod
    # def find_by_tags(*tags):
    #     ret_list = []
    #     for item_tag in tags:
    #         post_tag_list = PostsTag.query.filter_by(posts_tag=item_tag).all()
    #         ret_list.extend(post_tag_list)
    #
    #     return list(set(ret_list))


class PostsManage(object):

    def __init__(self, posts_id):
        pass


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
