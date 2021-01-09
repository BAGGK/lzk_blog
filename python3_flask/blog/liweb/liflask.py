from flask import Flask
from flask.blueprints import Blueprint
from blog.liweb.view import View
import inspect
import sys


class LiFlask(Flask):

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):

        if 'LOAD_MODELS' in self.config:
            for model in self.config['LOAD_MODELS']:
                # 加载模块
                __import__(model)
                # 获取 蓝图，如果配置了则使用配置了的，如果没有则新建
                blue_var = self.get_bp(model)
                class_list = inspect.getmembers(sys.modules[model + '.view'], inspect.isclass)

                for item_name, item_class in class_list:

                    if issubclass(item_class, View) and item_name != 'View':
                        url_path = item_class.__doc__.strip()

                        blue_var.add_url_rule(url_path,
                                              view_func=item_class.as_view(name=item_class.__name__))

                self.register_blueprint(blue_var, url_prefix='/api')
        # return super(LiFlask, self).run(host, port, debug, load_dotenv)

    def get_bp(self, model_name):

        # 从配置文件里面读取蓝图
        if self.config.get('LOAD_BLUEPRINT', None):
            bp_path: str = self.config['LOAD_BLUEPRINT'].get(model_name, None)
            if bp_path is not None:
                bp_path, bp_class_name = bp_path.rsplit('.', 1)
                __import__(bp_path)
                temp_var = inspect.getmembers(sys.modules[bp_path])[8]
                print(temp_var)
        # 如果没有则新建一个
        return Blueprint(model_name, model_name)
