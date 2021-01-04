from blog import db
from blog.global_class.model import DbBase


class Fitness(db.Model, DbBase):
    # id ，主要是为了优化查询
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(10), unique=True)
    weight = db.Column(db.Float)


# def create_test_data():
#     import time
#     time.localtime()
#     one_day_second = 24 * 60 * 60
#     for i in range(10):
#         time_str = time.strftime('%Y-%m-%d', time.localtime(time.time() - one_day_second * 10 + one_day_second * i))
#         Fitness(weight=150 - i, date=time_str).save()
