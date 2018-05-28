from datetime import datetime

from flask_socketio import emit
from sqlalchemy.orm.exc import NoResultFound
from app import api_root
from flask_restful import Resource
from app.model.OrderItem import OrderItem
from app import db


# 주문 처리 Class
@api_root.resource("/v1/orders/<int:order_id>/<string:status>")
class OrderController(Resource):
    # 주문 처리
    def put(self, order_id, status):
        try:
            order_item = OrderItem.query.filter(OrderItem.id == order_id).one()
        except NoResultFound as e:
            response = {
                "err": 1,
                "data": {}
            }
            return response
        order_item.status = status
        db.session.commit()

        emit('change order status', status)

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end="")
        print(" %d번 주문 처리 : " %order_id + status)
        response = {
            "err": 0,
            "data": {}
        }
        return response
