import os
from datetime import datetime

from jsonschema import validate

from app import api_root, APP_ROOT, app
from flask_restful import Resource
from flask import request
from app.model.Item import Item
from app import db
from sqlalchemy.orm.exc import NoResultFound


# 메뉴 상세 조회, 수정, 삭제 Class
@api_root.resource("/v1/items/<int:id>", endpoint='items')
class UpdateItem(Resource):
    # 메뉴 상세 조회
    def get(self, id):

        try:
            item = Item.query.filter(Item.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        response = {
            "err": 0,
            "data": {
                "itemId": item.id,
                "name": item.name,
                "price": item.price,
                "categoryId": item.categoryId
            }
        }
        return response

    # 메뉴 수정
    def put(self, id):
        json_data = request.get_json(force=True)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "integer"},
                "categoryId": {"type": "integer"}
            }
        }
        validate(json_data, schema)

        name = json_data['name']
        price = json_data['price']
        categoryId = json_data['categoryId']

        try:
            item = Item.query.filter(Item.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
        print(" 메뉴 수정 : 이름(" + item.name + "->" + name + "), 가격(" + str(item.price) + "->" + str(price) + ")")
        item.name = name
        item.price = price
        item.categoryId = categoryId

        db.session.commit()

        response = {
            "err": 0,
            "data": {}
        }
        return response


    # 메뉴 삭제
    def delete(self, id):

        try:
            item = Item.query.filter(Item.id == id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response

        print("<" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "> ", end="")
        print("메뉴 삭제 - " + item.name)
        db.session.delete(item)
        db.session.commit()
        response = {
            "err": 0,
            "data": {}
        }
        return response
