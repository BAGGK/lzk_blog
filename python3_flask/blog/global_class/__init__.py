from . import base_input, model, base_query
from .base_query import BaseQuery
from .base_input import BaseInput

from blog import app

if app.config['API_REDIS_CACHE']:
    from . import request_func
