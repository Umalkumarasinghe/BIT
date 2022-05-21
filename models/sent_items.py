from app import db
from flask import Blueprint
from flask_login import UserMixin

sent_sent_item_model_blueprint = Blueprint('sent_item_model_blueprint', __name__)

class sent_items(db.Model, UserMixin):
    __tablename__ = 'sent_items'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sent_item_name = db.Column(db.String(200))
    sent_item_quantity = db.Column(db.Integer)
    sent_item_unit_price = db.Column(db.Integer)

    # init function
    def __init__(self, sent_item_name, sent_item_quantity, sent_item_unit_price):

        self.sent_item_name = sent_item_name
        self.sent_item_quantity = sent_item_quantity
        self.sent_item_unit_price = sent_item_unit_price

    # returns object in string format
    def __repr__(self):
        return self.sent_item_name
