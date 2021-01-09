from blog import db
from blog.global_class import DbBase


class UrlPath(db.Model, DbBase):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module = db.Column(db.String(64))
    url_path = db.Column(db.String(128), unique=True)
    class_path = db.Column(db.String(128), unique=True)
