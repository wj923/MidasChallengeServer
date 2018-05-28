from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, INTEGER, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'extend_existing': True
    }

    id = db.Column(
        BIGINT(20, unsigned=True),
        primary_key=True,
        index=True
    )

    quantity = db.Column(
        INTEGER(10)
    )

    paymentDate = db.Column(
        TIMESTAMP
    )

    size = db.Column(
        VARCHAR(10)
    )

    userId = db.Column(
        BIGINT(20, unsigned=True),
        ForeignKey("User.id", ondelete="CASCADE")
    )

    itemId = db.Column(
        BIGINT(20, unsigned=True),
        ForeignKey("Item.id", ondelete="CASCADE")
    )

    status = db.Column(
        VARCHAR(20)
    )

    @hybrid_property
    def price(self):
        return self.itemId.price * self.quantity

    def as_dict(self):
        dict = {}
        for c in self.__table__.columns:
            if c.name == "paymentDate":
                tmp = getattr(self, c.name).__str__()
                dict[c.name] = tmp
            else:
                dict[c.name] = getattr(self, c.name)
        return dict