from app import db
from flask import Blueprint
from flask_login import UserMixin

production_order_line_line_model_blueprint = Blueprint('production_order_line_line_model_blueprint', __name__)


class ProductionOrderLine(db.Model, UserMixin):
    __tablename__ = 'production_order_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name_line = db.Column(db.String(10))
    item_quantity_line = db.Column(db.Integer)
    item_sent_quantity_line = db.Column(db.Integer)
    description = db.Column(db.String(120), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    production_team_id = db.Column(db.Integer, db.ForeignKey('production_team.id'))
    production_team = db.relationship("ProductionTeam")
    production_order_id = db.Column(db.Integer, db.ForeignKey('production_order.id'))
    production_order = db.relationship('ProductionOrder')

    def __init__(self, item_id, item_quantity_line, item_sent_quantity_line, item_name_line, production_order_line_id):
        self.item_id = item_id
        self.item_quantity_line = item_quantity_line
        self.item_name_line = item_name_line
        self.item_sent_quantity_line = item_sent_quantity_line
        self.production_order_line_id = production_order_line_id

    def __repr__(self):
        return self.item_id



