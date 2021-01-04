from blog import app, cache
from flask import request, g, Response
from redis import Redis


@app.before_request
def before_redis_cache():
    """API:fitness:url:argc"""
    redis_cache: Redis = cache

    if request.method == 'GET':
        key_name = request.path
        ret_val = redis_cache.get(key_name)
        if ret_val:
            g.is_redis_cache = True
            return ret_val
    elif request.method == 'POST':
        for i in cache.keys('*'):
            cache.delete(i)

    g.is_redis_cache = False


@app.after_request
def after_redis_cache(environ):
    environ: Response

    if g.is_redis_cache is True:
        return environ

    if request.method == 'GET' and environ.status_code == 200:
        redis_cache: Redis = cache
        redis_cache.set(request.path, environ.data)

    return environ
