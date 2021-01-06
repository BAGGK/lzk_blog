class BaseConfig(object):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://lzk_baggk:845613@127.0.0.1/lzk_baggk'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GAOKAO123@127.0.0.1:3306/blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOAD_MODELS = ['blog.fitness', 'blog.posts', 'blog.login']
    # LOAD_MODELS = ['blog.fitness']
    LOAD_BLUEPRINT = {
        'login': 'login.control.login_bp',
        'fitness': 'login.control.login_bp'
    }
    API_REDIS_CACHE = False


class DebugConfig(BaseConfig):
    pass


class RunConfig(BaseConfig):
    pass
