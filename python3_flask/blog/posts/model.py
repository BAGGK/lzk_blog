"""
Tag 和 posts 之间，其实是多对多的关系。 这是之前，我理解错了的地方。

一对多是：类似于一个班级可以有很多个学生，这个学生只能属于这个班级。

但是这个是不一样，一个文章可以有很多个 tag, 而且一个 tag 也可以有很多个 posts
"""
from blog import db
from blog.global_class.model import DbBase


class Posts(db.Model, DbBase):
    posts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文件原来的名字
    filename = db.Column(db.String(128), nullable=False)
    # 文件的存储地址
    up_time = db.Column(db.BigInteger, index=True)
    content_path = db.Column(db.String(15000))
    tags = db.relationship('Tag', secondary='posts_tag', backref=db.backref('posts_set'))


class PostsTag(db.Model, DbBase):
    pt_id = db.Column(db.Integer, primary_key=True)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.posts_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))


class Tag(db.Model, DbBase):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)

