from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, ENUM
from app import db


class User(db.Model):
    __tablename__ = 'User'
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

    username = db.Column(
        VARCHAR(128),
        unique=True
    )

    email = db.Column(
        VARCHAR(128)
    )

    phone = db.Column(
        VARCHAR(20)
    )

    password = db.Column(
        VARCHAR(128)
    )

    birthday = db.Column(
        DATETIME()
    )

    joinDate = db.Column(
        DATETIME()
    )

    authority = db.Column(
        VARCHAR(20)
    )

    def as_dict(self):
        dict = {}
        for c in self.__table__.columns:
            if c.name == "password":
                continue
            if c.name == "birthday":
                tmp = getattr(self, c.name).strftime("%Y-%m-%d")
                dict[c.name] = tmp
            else:
                if c.name == "joinDate":
                    tmp = getattr(self, c.name).__str__()
                    dict[c.name] = tmp
                else:
                    dict[c.name] = getattr(self, c.name)
        return dict
