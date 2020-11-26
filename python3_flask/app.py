from flask_cors import *
from setting import app

CORS(app, supports_credentials=True)
