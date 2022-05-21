from app import db
from flask import Blueprint
from flask_login import UserMixin

purchase_order_line_model_blueprint = Blueprint('purchase_order_line_model_blueprint', __name__)


class PurchaseOrderLine(db.Model, UserMixin):
    __tablename__ = 'purchase_order_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship("Supplier")
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    purchase_order = db.relationship('PurchaseOrder')

    def __init__(self, item_id, quantity, unit_price, purchase_order_id, subtotal):
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal
        self.purchase_order_id = purchase_order_id

    def __repr__(self):
        return self.item_id



