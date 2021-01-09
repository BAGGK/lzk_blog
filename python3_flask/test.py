from blog import db
from blog.fitness.model import *
from blog.posts.model import *

db.drop_all()
db.create_all()