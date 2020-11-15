# coding: utf-8

from liweb import View
from flask import request, render_template, json
from model import Fitness
import markdown
from config import app
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
        data = request.get_data()
        weight = data.split('=')[1]
        weight = float(weight)

        if weight < 100:
            weight *= 2

        Fitness.push(weight)
        return str(weight)


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
            print '0'
        else:
            return '1'


class IndexView(View):
    """
    /
    """
    methods = ['get']

    @staticmethod
    def get():
        ret_val = {
            'current_page': 0,
            'posts': [
                {
                    'url': "https://themes.gohugo.io//theme/anatole/post/markdown-syntax/",
                    'title': 'Markdown Syntax Guide',
                    'content': 'This article offers a sample of basic Markdown syntax that can be used in Hugo content files, also it shows whether basic HTML elements are decorated with CSS in a Hugo theme.',
                    'date': 'Mon, Mar 11, 2019',
                    'tags': [{
                        'tag_url': 'https://themes.gohugo.io//theme/anatole/tags/markdown/',
                        'tag_name': 'markdown'
                    },
                        {
                            'tags_url': 'https://themes.gohugo.io//theme/anatole/tags/css/',
                            'tag_name': 'css'
                        },
                        {
                            'tags_url': 'https://themes.gohugo.io//theme/anatole/tags/themes/',
                            'tag_name': 'themes'
                        }
                    ]
                }, {
                    'url': "https://themes.gohugo.io//theme/anatole/post/markdown-syntax/",
                    'title': 'python 语法',
                    'content': '这遍文章主要是介绍 python 的基础语法。比如 列表 字典 元组 集合',
                    'date': 'Mon, Mar 11, 2019',
                    'tags': [{
                        'tag_url': 'https://themes.gohugo.io//theme/anatole/tags/markdown/',
                        'tag_name': 'markdown'
                    },
                        {
                            'tags_url': 'https://themes.gohugo.io//theme/anatole/tags/css/',
                            'tag_name': 'css'
                        },
                        {
                            'tags_url': 'https://themes.gohugo.io//theme/anatole/tags/themes/',
                            'tag_name': 'themes'
                        }
                    ]
                }]}
        temp_var = ret_val['posts']
        print temp_var

        return json.dumps(ret_val)


class LoginView(View):
    "/login"
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