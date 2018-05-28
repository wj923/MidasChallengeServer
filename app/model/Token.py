from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Token(db.Model):

    __tablename__ = 'Token'
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

    token = db.Column(
        VARCHAR(256)
    )

    dueDate = db.Column(
        DATETIME()
    )

    userId = db.Column(
        BIGINT(20, unsigned=True),
        ForeignKey("User.id", ondelete="CASCADE")
    )

    userRow = relationship("User", lazy="joined")