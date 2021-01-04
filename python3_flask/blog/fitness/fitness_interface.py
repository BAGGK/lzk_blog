from blog.global_class.base_input import BaseInput
from .adapter import AdapterFactor
from .db_input import DBInput


class FitnessInterface(object):

    @staticmethod
    def input(fit_data, db_list=None):
        db_list = db_list if db_list else [DBInput]

        for each_class in db_list:
            if issubclass(each_class, BaseInput):
                each_class(fit_data).save()
            else:
                raise TypeError
        return None

    @staticmethod
    def output(query_instance):
        # 1. 得到查询的列表
        # 2. 遍历循环，全部转换成 FitnessContext

        db_list = query_instance.all()
        ret_list = []

        for each_ins in db_list:
            temp_var = AdapterFactor(each_ins)
            ret_list.append(temp_var)
        return ret_list
