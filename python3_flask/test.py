from threading import Thread
from redis import Redis
from blog.fitness.view import FitnessView

cache = Redis()

for i in cache.keys('*'):
    cache.delete(i)

print('helo')
print(cache.keys('*'))