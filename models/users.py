from app import db
import app
from flask import Blueprint
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

user_model_blueprint = Blueprint('user_model_blueprint', __name__)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    active = db.Column(db.Boolean)
    full_name = db.Column(db.String(200))
    calling_name = db.Column(db.String(50))
    last_login = db.Column(db.DateTime, nullable=True)
    last_logout = db.Column(db.DateTime, nullable=True)
    nic = db.Column(db.String(12), unique=True)
    contact_no = db.Column(db.String(20))
    address = db.Column(db.String(255))

    def get_reset_token(self, expires_sec=1800):
        serial = Serializer(app.SECRET_KEY, expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(app.SECRET_KEY)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, password, email, full_name, calling_name, last_login, last_logout, nic, contact_no, address, active=None):
        self.password = password or None,
        self.email = email,
        self.full_name = full_name
        self.calling_name = calling_name or None
        self.active = active
        self.last_login = last_login or None
        self.last_logout = last_logout or None
        self.nic = nic
        self.contact_no = contact_no
        self.address = address

    def __repr__(self):
        return self.email



