import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "secret"

db = SQLAlchemy(app)
socketio = SocketIO(app)

from app.model import *

db.create_all()

api_root = Api(app, catch_all_404s=True)

from app.api.v1 import *