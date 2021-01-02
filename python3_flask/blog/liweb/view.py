from flask import views


class MyType(views.MethodViewType):

    def __init__(cls, name, bases, d):
        super(MyType, cls).__init__(name, bases, d)


class View(views.MethodView):
    pass
