"""
    control the access of web
"""

from config import app


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run()
