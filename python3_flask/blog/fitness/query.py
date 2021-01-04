from blog.global_class.base_query import BaseQuery
from .model import Fitness, db

__all__ = ['FitnessQueryAll']


class FitnessQuery(BaseQuery):

    def __init__(self):
        self.class_type = Fitness

    def all(self):
        raise NotImplementedError


class FitnessQueryAll(FitnessQuery):

    def all(self):
        session = db.session
        return session.query(self.class_type).all()
