from blog.global_class.base_query import BaseQuery
from blog import db
from .model import Fitness

__all__ = ['FitnessQueryAll', 'FitnessDateQuery']


class FitnessQuery(BaseQuery):

    def __init__(self):
        self.class_type = Fitness

    def all(self):
        raise NotImplementedError


class FitnessQueryAll(FitnessQuery):

    def all(self):
        session = db.session
        return session.query(self.class_type).all()


class FitnessDateQuery(FitnessQuery):

    def __init__(self, date):
        self.date = date
        super(FitnessDateQuery, self).__init__()

    def all(self):
        session = db.session
        return session.query(self.class_type).filter(self.class_type.date == self.date).all()
