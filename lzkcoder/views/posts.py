from liweb import View
from flask import request
from config import app

import werkzeug.datastructures


class FileUpload(View):
    "/file_upload"

    methods = ["GET", "POST"]

    @staticmethod
    def get():
        return 'hello'

    @staticmethod
    def post():
        f = request.files['file_name']
        f.save(app.root_path + '/posts/' + f.filename)
        print app.root_path + '/posts/' + f.filename
        return "ok", 200


