from liweb import LiFlask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *

app = LiFlask(__name__)
# Config of model
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lzk_baggk:845613@127.0.0.1/lzk_baggk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The handle of the model
db = SQLAlchemy(app)

CORS(app, supports_credentials=True)
