class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://lzk_baggk:845613@127.0.0.1/lzk_baggk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOAD_MODELS = ['fitness', 'posts']


class DebugConfig(BaseConfig):
    pass


class RunConfig(BaseConfig):
    pass