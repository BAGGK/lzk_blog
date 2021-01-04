from blog.global_class.base_query import BaseQuery
from blog import db
from .model import Fitness

__all__ = ['FitnessQueryAll', 'FitnessDateQuery']


class FitnessQuery(BaseQuery):

    def __init__(self):
        self.class_type = Fitness
        self.query_ins = db.session.query(Fitness)

    def all(self):
        self.filter()
        self.sort_and_limit()
        return self.query_ins.all()

    def sort_and_limit(self):
        if hasattr(self, 'desc') and self.desc is True:
            self.query_ins = self.query_ins.order_by(self.class_type.id.desc())

        if hasattr(self, 'limit'):
            self.query_ins = self.query_ins.limit(self.limit)

    def filter(self):
        if hasattr(self, 'max_date'):
            self.query_ins = self.query_ins.filter(self.class_type.date <= self.max_date)

        if hasattr(self, 'min_date'):
            self.query_ins = self.query_ins.filter(self.class_type.date >= self.min_date)

        if hasattr(self, 'date'):
            self.query_ins = self.query_ins.filter(self.class_type.date == self.date)


class FitnessQueryAll(FitnessQuery):

    def __init__(self, limit=10):
        super(FitnessQueryAll, self).__init__()
        self.limit = limit
        self.desc = True


class FitnessDateQuery(FitnessQuery):

    def __init__(self, date):
        super(FitnessDateQuery, self).__init__()
        self.date = date
