from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Config of model
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lzk_baggk:845613@127.0.0.1/lzk_baggk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# The handle of the model
db = SQLAlchemy(app)

