from flask import request


class MetaClass(type):

    def __call__(cls, argc_name, is_list=False):
        # 如果是 get 则从 argc 里面取值，如果是 post 则从 form 中取值
        argc_dict = request.args if request.method == 'GET' else request.form
        cls.ret_val = argc_dict.getlist(argc_name) if is_list else argc_dict.get(argc_name)

        return super(MetaClass, cls).__call__(argc_name, is_list)


class IntegerField(metaclass=MetaClass):
    def __new__(cls, argc_name, is_list=False):
        try:
            cls.ret_val = list(map(int, cls.ret_val)) if isinstance(cls.ret_val, list) else int(cls.ret_val)
        except (ValueError, TypeError):
            cls.ret_val = False

        return cls.ret_val


class StringField(metaclass=MetaClass):
    def __new__(cls, argc_name, is_list=False):
        return cls.ret_val


class FileField(object):
    def __new__(cls, argc_name, is_list=False):
        argc_dict = request.files
        cls.ret_val = argc_dict.getlist(argc_name) if is_list else argc_dict.get(argc_name)

        return cls.ret_val
