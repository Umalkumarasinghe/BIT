# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

reordering_model_blueprint = Blueprint('reordering_model_blueprint', __name__)

# initiating the class
class Reordering(db.Model, UserMixin):
    __tablename__ = 'reordering'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    maximum_quantity = db.Column(db.Integer)
    minimum_quantity = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    supplier = db.relationship("Supplier")
    item = db.relationship("Items")

    # init function
    def __init__(self, supplier_id, item_id, maximum_quantity, minimum_quantity):

        self.supplier_id = supplier_id
        self.item_id = item_id
        self.maximum_quantity = maximum_quantity
        self.minimum_quantity = minimum_quantity

    # returns object in string format
    def __repr__(self):
        return self.item_id