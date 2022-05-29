from app import db
from flask import Blueprint
from flask_login import UserMixin

grn_line_model_blueprint = Blueprint('grn_line_model_blueprint', __name__)


class GrnLine(db.Model, UserMixin):
    __tablename__ = 'grn_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    demand_quantity = db.Column(db.Integer)
    received_quantity = db.Column(db.Integer)
    remaining_quantity = db.Column(db.String(120), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    grn_id = db.Column(db.Integer, db.ForeignKey('grn.id'))
    grn = db.relationship('Grn')

    def __init__(self, item_id, demand_quantity, received_quantity, remaining_quantity, grn_id):
        self.item_id = item_id
        self.demand_quantity = demand_quantity
        self.received_quantity = received_quantity
        self.remaining_quantity = remaining_quantity
        self.grn_id = grn_id

    def __repr__(self):
        return self.item_id



