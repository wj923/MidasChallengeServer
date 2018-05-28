from datetime import datetime
from app import api_root
from flask_restful import Resource
from flask import request
from app.model.Item import Item
from jsonschema import validate
from app import db
from sqlalchemy.orm.exc import NoResultFound


# 전체 메뉴 조회 및 메뉴 등록 Class
@api_root.resource("/v1/items")
class RegisterItem(Resource):
    # 메뉴 전체 조회
    def get(self):
        list = []
        if request.args.get('category') is not None:
            category = request.args.get('category', type=int)
            item = Item.query.filter(Item.categoryId == category).all()
        else:
            item = Item.query.all()

        for x in item:
            list.append(x.as_dict())

        response = {
            "err": 0,
            "data": list
        }
        return response

    # 메뉴 등록
    def post(self):
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
            item = Item.query.filter(Item.name == name).one()
        except NoResultFound as e:
            item = Item(name=name, price=price, categoryId=categoryId)

            db.session.add(item)
            db.session.commit()

            print("item.id : %d" % item.id)

            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
            print(" 메뉴 등록 : " + name)

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
