# coding: utf-8
from setting import db
import os
import markdown
from flask_sqlalchemy import BaseQuery


class Posts(db.Model):
    posts_uuid = db.Column(db.String, primary_key=True)
    posts_title = db.Column(db.String)
    posts_head = db.Column(db.String)
    posts_ctime = db.Column(db.BigInteger, index=True)
    posts_mtime = db.Column(db.BigInteger)
    posts_tags = db.Column(db.String)
    # posts_filename = db.Column(db.String, nullable=False)
    posts_html = db.Column(db.String)

    def __init__(self, fd, posts_tags):
        """

        :type fd: file
        """
        if not isinstance(fd, file):
            raise TypeError('fd must be a file')
        # 以下是实例传递参数
        self.fd = fd
        # end
        posts_title, posts_head, posts_ctime, posts_mtime = self.__parse_file_head()
        self.posts_uuid = os.path.basename(fd.name)
        self.posts_title = posts_title
        self.posts_head = posts_head
        self.posts_ctime = posts_ctime
        self.posts_mtime = posts_mtime
        self.posts_tags = posts_tags
        # self.posts_filename = file_name
        self.posts_html = self.__md_to_html()

    def __md_to_html(self):
        self.fd.seek(0)
        md_unicode = self.fd.read().decode('utf-8')

        return markdown.markdown(md_unicode, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

    def __parse_file_head(self):
        fd = self.fd
        if not isinstance(fd, file):
            raise TypeError('The fd must be a file instance')

        posts_title = fd.readline().lstrip('# ').strip()
        posts_head = fd.readline().strip()
        while posts_head == '':
            posts_head = fd.readline().strip()
        posts_ctime = os.path.getctime(fd.name)
        posts_mtime = os.path.getmtime(fd.name)
        return posts_title, posts_head, posts_ctime, posts_mtime

    # 以下是外部接口
    @staticmethod
    def get_recent_posts(limit_num=30):
        return Posts.query.order_by(Posts.posts_ctime).limit(limit_num).all()

    @staticmethod
    def push(fd, tags):
        if not (isinstance(fd, file) and isinstance(tags, list)):
            raise TypeError

        new_data = Posts(fd, tags)
        db.session.add(new_data)
        db.session.commit()

    @staticmethod
    def pop(uuid):
        Posts.query.filter_by(uuid)

    @staticmethod
    def get_html(uuid):
        ret_var = db.session.query(Posts.posts_html).filter(Posts.posts_uuid == uuid).first()  # type: Posts

        ret_var = '<link rel="stylesheet" href="blog.css">' + ret_var.posts_html
        if ret_var:
            return ret_var
        else:
            return None


db.create_all()

