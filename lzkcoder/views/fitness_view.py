# coding: utf-8

from liweb import View
from flask import request, render_template, json
from model import Fitness
import markdown
from config import app
import time
import tool


class FitnessView(View):
    """
        /fitness/
    """
    methods = ['get', 'post']

    @staticmethod
    def get():

        date_list = []
        weight_list = []

        for each_item in Fitness.find_all():
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
        Fitness.push(weight)
        return 'ok', 200


class IsFitnessInput(View):
    """
    /is_fitness_input/
    """

    methods = ['GET']

    @staticmethod
    def get():
        current_data = time.strftime('%Y-%m-%d')
        temp_var = Fitness.find_one(current_data)
        if temp_var is None:
            return '0'
        else:
            return '1'


class IndexView(View):
    """
    /
    """
    methods = ['get']

    @staticmethod
    def get():
        return 'hello'


class LoginView(View):
    """/login"""
    method = ['get', 'post']

    @staticmethod
    def get():
        return 'hello'

    @staticmethod
    def post():
        pass


class PostShow(View):
    """
    /post_show
    """
    methods = ['get']

    @staticmethod
    def get():
        fd_str = open(app.root_path + '/posts/' + 'test_file.md').read().decode('utf-8')
        md_str = markdown.markdown(fd_str)
        print md_str
        return md_str
