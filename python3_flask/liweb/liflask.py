from flask import Flask
from flask.blueprints import Blueprint
from liweb.view import View
import inspect
import sys


class LiFlask(Flask):

    def run_old(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        for view in self.config['LOAD_MODELS']:
            __import__(view)
        for each_view in View.__subclasses__():
            try:
                self.add_url_rule(
                    each_view.__doc__.strip(),
                    view_func=each_view.as_view(name=each_view.__name__)
                )
            except Exception as e:
                print(each_view, e)
                exit()
        super(LiFlask, self).run(host, port, debug, load_dotenv)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):

        for model in self.config['LOAD_MODELS']:
            blue_var = Blueprint(model, model)
            __import__(model)
            class_list = inspect.getmembers(sys.modules[model + '.view'], inspect.isclass)
            for item_name, item_class in class_list:
                if issubclass(item_class, View) and item_name != 'View':
                    try:
                        blue_var.add_url_rule(
                            item_class.__doc__.strip(),
                            view_func=item_class.as_view(name=item_class.__name__)
                        )
                    except Exception as e:
                        print(item_class, e)
            self.register_blueprint(blue_var)
        return super(LiFlask, self).run(host, port, debug, load_dotenv)
