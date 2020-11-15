from config import db
import time
import flask_sqlalchemy


def formatted_time():
    return time.strftime('%Y-%m-%d', time.localtime())


class Fitness(db.Model):
    """
    class object is table , and the instance object is column
    """
    __tablename__ = 'fitness'
    weight = db.Column(db.Float)
    date = db.Column(db.String, primary_key=True)

    def __init__(self, weight, date=None):
        self.weight = weight
        self.date = formatted_time() if date is None else date

    @staticmethod
    def push(weight):
        db.session.add(Fitness(weight))
        db.session.commit()

    @staticmethod
    def pop(date):
        delete_var = Fitness.find_one(date)
        db.session.delete(delete_var)
        db.session.commit()

    @staticmethod
    def find_one(date, filters=None):
        return db.session.query(Fitness). \
            filter(Fitness.date == date).first()

    @staticmethod
    def find_all(find_days=30):
        """

        :rtype: list[Fitness]
        """
        return db.session.query(Fitness).all()[:find_days]


class FitnessFilter(object):
    pass


if __name__ == '__main__':
    temp_var = db.session.query(Fitness)  # type: flask_sqlalchemy.BaseQuery
    var_1 = temp_var.filter(Fitness.date == '2020-10-01')  # type: flask_sqlalchemy.BaseQuery
    print var_1.first()
