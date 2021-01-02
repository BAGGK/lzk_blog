from blog.liweb import View
from flask import request


class LoginView(View):
    """
    /login/
    """
    methods = ['post']

    @staticmethod
    def post():
        user_id = request.form.get('user_id', None)
        password = request.form.get('password', None)

        # 合法性
        if not (user_id and password):
            return 403, '你必须输入合法的密码或者'
        else:
            result = LoginView.__verify(user_id, password)
            if result:
                # do some thing
                return 'ok', 200
            else:
                return 'user_id or password error'

    @staticmethod
    def __verify(user_id, password):
        if user_id == 'lzk' and password == '845613':
            return True
        else:
            return False


