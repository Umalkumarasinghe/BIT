from app import db
from flask import Blueprint
from flask_login import UserMixin

grn_model_blueprint = Blueprint('grn_model_blueprint', __name__)


class Grn(db.Model, UserMixin):
    __tablename__ = 'grn'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    grn_name = db.Column(db.String(200))
    grn_created_date = db.Column(db.Date)
    grn_expected_date = db.Column(db.Date)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    grn_state = db.Column(db.String(120))
    supplier = db.relationship("Supplier")
    item = db.relationship("Items")
    purchase_order = db.relationship("PurchaseOrder")
    grn_line = db.relationship("GrnLine", backref="grn_line", lazy='dynamic')

    def __init__(self, supplier_id, grn_created_date, grn_expected_date, grn_state=None, po_id=None):
        self.grn_created_date = grn_created_date
        self.grn_expected_date = grn_expected_date
        self.supplier_id = supplier_id
        self.grn_state = grn_state
        self.purchase_order_id = po_id
        # self.active = active

    def __repr__(self):
        return self.grn_name



