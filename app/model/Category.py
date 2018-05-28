from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from app import db


class Category(db.Model):
    __tablename__ = 'Category'
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

    name = db.Column(
        VARCHAR(128)
    )