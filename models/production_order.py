from app import db
from flask import Blueprint
from flask_login import UserMixin

production_order_model_blueprint = Blueprint('production_order_model_blueprint', __name__)


class ProductionOrder(db.Model, UserMixin):
    __tablename__ = 'production_order'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    production_order_name = db.Column(db.String(200))
    production_order_created_date = db.Column(db.Date)
    production_order_expected_date = db.Column(db.Date)
    production_team_id = db.Column(db.Integer, db.ForeignKey('production_team.id'))
    production_team = db.relationship("ProductionTeam")
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    production_order_state = db.Column(db.String(120), default='Pending')

    item = db.relationship("Items")
    production_order_line = db.relationship("ProductionOrderLine", backref="production_order_line", lazy='dynamic')


    def __init__(self,production_team_id, production_order_name, production_order_created_date, production_order_expected_date, production_order_state=None):
        self.production_order_name = production_order_name,
        self.production_order_created_date = production_order_created_date
        self.production_order_expected_date = production_order_expected_date
        self.production_team_id = production_team_id
        self.production_order_state = production_order_state
        # self.active = active

    def __repr__(self):
        return self.production_order_name



