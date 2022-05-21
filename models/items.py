# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

item_model_blueprint = Blueprint('item_model_blueprint', __name__)

# initiating the class
class Items(db.Model, UserMixin):
    __tablename__ = 'items'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.String(200))
    item_code = db.Column(db.String(120), unique=True)
    item_quantity = db.Column(db.Integer)
    item_unit_price = db.Column(db.Integer)

    # init function
    def __init__(self, item_name, item_code, item_quantity, item_unit_price):

        self.item_name = item_name
        self.item_code = item_code
        self.item_quantity = item_quantity
        self.item_unit_price = item_unit_price

    # returns object in string format
    def __repr__(self):
        return self.item_name



