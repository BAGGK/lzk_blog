from flask import Flask, views, render_template

app = Flask(__name__)


@app.route('/')
def index():
    user = {
        'username': 'lzk',
        'bio': 'A bo who loves movies and music'
    }
    return render_template('../templates/index.html')
