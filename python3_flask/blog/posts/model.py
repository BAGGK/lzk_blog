from blog import db
from blog.global_class.model import DbBase


class Posts(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文件原来的名字
    posts_filename = db.Column(db.String(128), nullable=False)
    # 文件的存储地址
    posts_path = db.Column(db.String(128))


class PostsTag(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, primary_key=True)


class Tag(db.Model, DbBase):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(128), unique=True)
