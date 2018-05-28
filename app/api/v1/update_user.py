from datetime import datetime
from app import api_root
from flask_restful import Resource
from flask import request
from app.model.User import User
from jsonschema import validate
from app import db
from sqlalchemy.orm.exc import NoResultFound


# 사용자 정보 상세 조회, 수정, 삭제 Class
@api_root.resource("/v1/users/<int:id>", endpoint='users')
class UpdateItem(Resource):
    # 사용자 정보 상세 조회
    def get(self, id):

        try:
            user = User.query.filter(User.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        print("조회 성공 : " + user.name)
        response = {
            "err": 0,
            "data": {
                "name": user.name,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "password": user.password,
                "birthday": user.birthday.strftime("%Y/%m/%d")
            }
        }
        return response

    # 사용자 정보 수정
    def put(self, id):
        json_data = request.get_json(force=True)

        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "phone": {"type": "string"}
            }
        }
        validate(json_data, schema)

        email = json_data['email']
        phone = json_data['phone']

        try:
            user = User.query.filter(User.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
        print(" 사용자 정보 수정 : " + user.name)
        user.email = email
        user.phone = phone

        db.session.commit()
        response = {
            "err": 0,
            "data": {}
        }
        return response

    # 메뉴 삭제
    def delete(self, id):

        try:
            user = User.query.filter(User.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        db.session.delete(user)
        db.session.commit()
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
        print(" 사용자 정보 삭제 : " + user.name)
        response = {
            "err": 0,
            "data": {}
        }
        return response
