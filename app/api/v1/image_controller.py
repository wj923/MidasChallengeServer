import os
from app import api_root, APP_ROOT
from flask_restful import Resource
from flask import send_file, request, redirect, url_for


# 이미지 처리 Class
@api_root.resource("/images/<string:file_name>", endpoint='images')
class ImageController(Resource):

    def get(self, file_name):
        try:
            target = os.path.join(APP_ROOT, 'images', file_name)
            return send_file(target)
        except FileNotFoundError:
            return None


'''    def put(self, file_name):
        target = os.path.join(APP_ROOT, 'images')
        file = request.files['file']
        file.save(target, file_name)
        return redirect(url_for('put', filename=file_name))

    def post(self, file_name):
        target = os.path.join(APP_ROOT, 'images')
        file = request.files['file']
        file.save(target, file_name)
        return redirect(url_for('put', filename=file_name))'''
