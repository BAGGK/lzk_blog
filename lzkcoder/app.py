"""
    control the access of web
"""

from config import app


if __name__ == '__main__':
    app.run(view_package='views')

