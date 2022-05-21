from app import db
from flask import Blueprint
from flask_login import UserMixin

grn_line_model_blueprint = Blueprint('grn_line_model_blueprint', __name__)


class GrnLine(db.Model, UserMixin):
    __tablename__ = 'grn_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name_line = db.Column(db.String(10))
    item_quantity_line = db.Column(db.Integer)
    item_received_quantity_line = db.Column(db.Integer)
    description = db.Column(db.String(120), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship("Supplier")
    grn_id = db.Column(db.Integer, db.ForeignKey('grn.id'))
    grn = db.relationship('Grn')

    def __init__(self, item_id, item_quantity_line, item_received_quantity_line, item_name_line, grn_id):
        self.item_id = item_id
        self.item_quantity_line = item_quantity_line
        self.item_name_line = item_name_line
        self.item_received_quantity_line = item_received_quantity_line
        self.grn_id = grn_id

    def __repr__(self):
        return self.item_id



