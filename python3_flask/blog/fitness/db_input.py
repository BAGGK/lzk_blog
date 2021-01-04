from blog.global_class.base_input import BaseInput
from .fitness_context import FitnessContext
from .model import Fitness
from blog import db
import time


class DBInput(BaseInput):
    """
    _date : 是 "2021-01-01" 类型的字符串
    _time : 是时间戳
    """

    def save(self):
        data: FitnessContext = self.data

        session: db.Session = db.session
        last_fit = session.query(Fitness).order_by(Fitness.id.desc()).first()
        temp_list = []
        if last_fit:
            last_weight, last_date = last_fit.weight, last_fit.date

            interval_day = self.__get_interval_time(last_date)

            interval_weight = (data.weight - last_fit.weight) / interval_day
            interval_weight = interval_weight

            for i in range(1, interval_day):
                temp_weight = round(last_weight + i * interval_weight, 1)  # 保留一位小数
                temp_date = self.__change_date(last_date, i)
                temp_list.append(Fitness(weight=temp_weight, date=temp_date))

        # 确保今天输入的数据是准确的。
        now_fit = Fitness(date=data.date, weight=data.weight)
        temp_list.append(now_fit)
        session.add_all(temp_list)
        try:
            session.commit()
        except Exception as e:
            print('save error', e)
            session.rollback()

    def __get_interval_time(self, last_date):
        now_time = self.__str_time(self.data.date)
        last_time = self.__str_time(last_date)

        interval_day = int((now_time - last_time) / (24 * 60 * 60))
        return interval_day

    def __change_date(self, unchanged_date, interval_time):
        last_date = self.__str_time(unchanged_date)
        return time.strftime('%Y-%m-%d', time.localtime(last_date + interval_time * 60 * 24 * 60))

    @staticmethod
    def __str_time(now_data):
        now_date = time.strptime(now_data, '%Y-%m-%d')
        return time.mktime(now_date)
