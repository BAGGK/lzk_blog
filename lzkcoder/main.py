import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index2.html')

