from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, INTEGER
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Item(db.Model):
    __tablename__ = 'Item'
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

    # 이미지 추가

    name = db.Column(
        VARCHAR(128)
    )

    price = db.Column(
        INTEGER(10)
    )

    categoryId = db.Column(
        BIGINT(20, unsigned=True),
        ForeignKey("Category.id", ondelete="CASCADE")
    )

    categoryRow = relationship("Category", lazy="joined")

    def as_dict(self):
        dict = {}
        for c in self.__table__.columns:
            dict[c.name] = getattr(self, c.name)

        return dict