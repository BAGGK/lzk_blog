from blog import db
from blog.global_class.model import DbBase


class Fitness(db.Model, DbBase):
    # id ，主要是为了优化查询
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(10), unique=True)
    weight = db.Column(db.Float)

    # 添加配置设置编码
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
