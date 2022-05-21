from app import db
from flask import Blueprint
from flask_login import UserMixin

received_received_item_model_blueprint = Blueprint('received_item_model_blueprint', __name__)

class received_items(db.Model, UserMixin):
    __tablename__ = 'received_items'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    received_item_name = db.Column(db.String(200))
    received_item_quantity = db.Column(db.Integer)
    received_item_unit_price = db.Column(db.Integer)

    # init function
    def __init__(self, received_item_name, received_item_quantity, received_item_unit_price):

        self.received_item_name = received_item_name
        self.received_item_quantity = received_item_quantity
        self.received_item_unit_price = received_item_unit_price

    # returns object in string format
    def __repr__(self):
        return self.received_item_name
