# coding: utf-8

from blog.liweb import View
from flask import request, json
import time
from blog import tool
from .fitness_interface import FitnessInterface
from .query import FitnessQueryAll, FitnessDateQuery
from .fitness_context import FitnessContext
from .db_input import DBInput


class FitnessView(View):
    """
        /fitness/
    """
    methods = ['get', 'post']

    @staticmethod
    def get():
        fit_ctx = FitnessInterface.output(FitnessQueryAll())
        date_list = []
        weight_list = []

        for each_item in fit_ctx:
            date_list.append(each_item.date[-2:])
            weight_list.append(each_item.weight)

        ret_dic = {
            'weights': weight_list,
            'date': date_list
        }
        return json.dumps(ret_dic)

    @staticmethod
    def post():
        weight = request.form['input_weight']

        weight = tool.safe_float(weight)
        if weight is None:
            return '请输入数字', 400

        weight = weight * 2 if weight < 100 else weight

        temp_var = FitnessContext(weight=weight)
        FitnessInterface.input(temp_var, [DBInput])
        return 'ok', 200


class IsFitnessInput(View):
    """
    /is_fitness_input/
    """

    methods = ['GET']

    @staticmethod
    def get():
        current_data = time.strftime('%Y-%m-%d')
        temp_var = FitnessInterface.output(FitnessDateQuery(current_data))

        return '1' if temp_var else '0'
