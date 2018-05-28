import calendar
from datetime import datetime

from flask_socketio import emit
from sqlalchemy import desc, and_
from app import api_root
from flask_restful import Resource
from flask import request
from app.model.OrderItem import OrderItem
from app.model.User import User
from app.model.Item import Item
from jsonschema import validate
from app import db


# 전체 주문 조회 및 주문 등록 Class
@api_root.resource("/v1/orders")
class Order(Resource):
    # 주문 조회
    def get(self):
        list = []
        if request.args.get('userid') is not None:
            userid = request.args.get('userid')
            year = request.args.get('year')
            month = request.args.get('month')
            start = year+'-'+month+'-1'
            end = year+'-'+month+'-31'
            order_item = OrderItem.query.order_by(desc(OrderItem.paymentDate))\
                .filter(and_(OrderItem.userId == userid, start <= OrderItem.paymentDate, end >= OrderItem.paymentDate)).all()

        else:
            order_item = OrderItem.query.order_by(desc(OrderItem.paymentDate)).all()

        for x in order_item:
            dict = {'orderId': x.id, 'quantity': x.quantity, 'paymentDate': x.paymentDate.__str__(), 'size': x.size,
                    'status': x.status}

            user = User.query.filter(User.id == x.userId).one()
            dict['name'] = user.name
            dict['username'] = user.username

            item = Item.query.filter(Item.id == x.itemId).one()
            dict['itemname'] = item.name
            size_up = 0
            if x.size == "L":
                size_up += 500
            elif x.size == "XL":
                size_up += 1000
            dict['price'] = (item.price + size_up) * x.quantity

            list.append(dict)

        # 주문 내역 없음
        if len(list) == 0:
            response = {
                "err": 1,
                "data": {}
            }
        else:
            response = {
                "err": 0,
                "data": list
            }
        return response

    # 주문 등록
    def post(self):
        json_data = request.get_json(force=True)

        schema = {
            "type": "object",
            "properties": {
                "quantity": {"type": "integer"},
                "size": {"type": "string"},
                "userId": {"type": "integer"},
                "itemId": {"type": "integer"}
            }
        }

        validate(json_data, schema)

        quantity = json_data['quantity']
        paymentDate = datetime.now()
        size = json_data['size']
        userId = json_data['userId']
        itemId = json_data['itemId']
        status = "new"

        order_item = OrderItem(quantity=quantity, paymentDate=paymentDate, \
                               size=size, userId=userId, itemId=itemId, status=status)
        db.session.add(order_item)
        db.session.commit()

        emit('add order')

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
        print(" 주문 예약")

        response = {
            "err": 0,
            "data": {}
        }
        return response
