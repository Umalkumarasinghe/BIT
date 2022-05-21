from app import db
from flask import Blueprint
from flask_login import UserMixin

purchase_order_model_blueprint = Blueprint('purchase_order_model_blueprint', __name__)


class PurchaseOrder(db.Model, UserMixin):
    __tablename__ = 'purchase_order'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    purchase_order_name = db.Column(db.String(200))
    purchase_order_created_date = db.Column(db.Date)
    purchase_order_expected_date = db.Column(db.Date)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    purchase_order_state = db.Column(db.String(120), default='Pending')
    supplier = db.relationship("Supplier")
    item = db.relationship("Items")
    purchase_order_line = db.relationship("PurchaseOrderLine", backref="purchase_order_line", lazy='dynamic')
    purchase_total = db.Column(db.Integer)

    def __init__(self, supplier_id, purchase_order_name, purchase_order_created_date, purchase_order_expected_date, purchase_total, purchase_order_state=None):
        self.purchase_order_name = purchase_order_name,
        self.purchase_order_created_date = purchase_order_created_date
        self.purchase_order_expected_date = purchase_order_expected_date
        self.supplier_id = supplier_id
        self.purchase_order_state = purchase_order_state
        self.purchase_total = purchase_total

    def __repr__(self):
        return self.purchase_order_name



