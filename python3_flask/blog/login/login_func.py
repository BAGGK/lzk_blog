import inspect
import sys
from blog import app
from blog.liweb import View


@app.before_first_request
def get_url_path():
    for each_model in app.config['LOAD_MODELS']:
        class_name, class_type = inspect.getmembers(sys.modules[each_model + '.view'], inspect.isclass)

        if issubclass(class_type, View):
            class_path = each_model + '.view.' + class_name
