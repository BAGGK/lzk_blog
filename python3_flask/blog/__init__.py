from blog.liweb import LiFlask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from config import RunConfig
from flask_cors import *


app = LiFlask(__name__)

# load config object
app.config.from_object(RunConfig)
# The handle of the model
db = SQLAlchemy(app)
# The handle of the cache [redis]
cache = Redis()
# CORS
CORS(app, supports_credentials=True)
