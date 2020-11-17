# coding: utf-8
from config import db
import os
import flask
from flask_sqlalchemy import BaseQuery


class PostHead(db.Model):
    __tablename__ = 'post_head'

    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.String)
    post_time = db.Column(db.BigInteger, index=True)
    post_tags = db.Column(db.String)

    def __init__(self, post_title, post_content, post_time, post_tags):
        self.post_title = post_title
        self.post_content = post_content
        self.post_time = post_time
        self.post_tags = post_tags

    @staticmethod
    def parse_file_head(fd):
        if not isinstance(fd, file):
            raise TypeError('The fd must be a file instance')

        post_title = fd.readline().lstrip('# ').strip()
        post_content = fd.readline().strip()
        while post_content == '':
            post_content = fd.readline().strip()
        post_time = os.path.getctime(fd.name)
        return post_title, post_content, post_time

    @staticmethod
    def push(post_title, post_content, post_time, post_tags):
        new_data = PostHead(post_title, post_content, post_time, post_tags)
        db.session.add(new_data)
        db.session.commit()

    @staticmethod
    def get_recent_data(limit_num=30):
        return PostHead.query.order_by(PostHead.post_time).limit(limit_num).all()


if __name__ == '__main__':
    fd = open('../posts/test_file.md')
    temp_var = PostHead.parse_file_head(fd)
    for each_item in temp_var:
        print each_item

    tags = ['markdown', 'css', 'python']
    tags = flask.json.dumps(tags)
    temp_var = list(temp_var)
    temp_var.append(tags)
    PostHead.push(*temp_var)
