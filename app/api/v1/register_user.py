import hashlib
from datetime import datetime
from app import api_root
from flask_restful import Resource
from flask import request
from app.model.User import User
from jsonschema import validate
from app import db
from sqlalchemy.orm.exc import NoResultFound


# 전체 사용자 조회 및 사용자 등록 Class
@api_root.resource("/v1/users")
class RegisterUser(Resource):
    # 사용자 전체 조회
    def get(self):
        list = []
        user = User.query.all()
        for x in user:
            if x.authority != "admin":
                list.append(x.as_dict())

        response = {
            "err": 0,
            "data": list
        }
        return response

    # 사용자 등록
    def post(self):
        json_data = request.get_json(force=True)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "password": {"type": "string"},
                "birthday": {"type": "string"}
            }
        }

        validate(json_data, schema)

        name = json_data['name']
        username = json_data['username']
        email = json_data['email']
        phone = json_data['phone']
        password = json_data['password']
        birthday = json_data['birthday']
        authority = "member"

        join_date = datetime.now().strftime("%y/%m/%d")
        join_date = str(join_date)

        password_hashSHA = hashlib.sha256()
        password_hashSHA.update((password + join_date).encode('utf-8'))
        password = password_hashSHA.hexdigest()

        try:
            user = User.query.filter(User.username == username).one()
        except NoResultFound as e:
            user = User(name=name, username=username, password=password, email=email, phone=phone,\
                        birthday=birthday, joinDate=datetime.now(), authority=authority)

            db.session.add(user)
            db.session.commit()

            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
            print(" 사용자 등록 : " + name)

            response = {
                "err": 0,
                "data": {}
            }
            return response

        response = {
            "err": 1,
            "data": {}
        }
        return response
