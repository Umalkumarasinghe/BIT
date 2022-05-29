from app import db
from flask import Blueprint
from flask_login import UserMixin

production_line_model_blueprint = Blueprint('production_line_model_blueprint', __name__)


class ProductionLine(db.Model, UserMixin):
    __tablename__ = 'production_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    demand_quantity = db.Column(db.Integer)
    received_quantity = db.Column(db.Integer)
    remaining_quantity = db.Column(db.String(120), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    production_id = db.Column(db.Integer, db.ForeignKey('production.id'))
    production = db.relationship('Production')

    def __init__(self, item_id, demand_quantity, production_id):
        self.item_id = item_id
        self.demand_quantity = demand_quantity
        self.production_id = production_id

    def __repr__(self):
        return self.item_id



