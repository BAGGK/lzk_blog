from flask import Flask
from liweb.view import View


class LiFlask(Flask):

    def run(self, host=None, port=None, debug=None, load_dotenv=True, view_package=None, **options):
        __import__(view_package)
        for each_view in View.__subclasses__():
            try:
                self.add_url_rule(
                    each_view.__doc__.strip(),
                    view_func=each_view.as_view(name=each_view.__name__)
                )
            except Exception, e:
                print each_view, e
                exit()
        super(LiFlask, self).run(host, port, debug, load_dotenv)
