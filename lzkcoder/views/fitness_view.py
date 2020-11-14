from liweb import View
from flask import request, render_template
from model import Fitness

from datetime import datetime
import time


def date_change(date, interval):
    time_tuple = time.strptime(date, '%Y-%m-%d')
    time_s = time.mktime(time_tuple) + interval * 60 * 60 * 24
    new_date = time.strftime('%Y-%m-%d', time.localtime(time_s))

    return new_date


class FitnessView(View):
    """
        /fitness/
    """
    methods = ['get', 'post']

    @staticmethod
    def get():
        return 'hello'

    @staticmethod
    def post():
        data = request.get_data()
        weight = data.split('=')[1]
        weight = float(weight)

        if weight < 100:
            weight *= 2

        Fitness.push(weight)
        return str(weight)


class IndexView(View):
    """
    /
    """
    methods = ['get']

    @staticmethod
    def get():
        return render_template('index.html')


class LoginView(View):
    "/lzk"
    method = ['get', 'post']

    @staticmethod
    def post():
        pass
