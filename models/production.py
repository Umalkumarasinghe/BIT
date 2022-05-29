from app import db
from flask import Blueprint
from flask_login import UserMixin

production_model_blueprint = Blueprint('production_model_blueprint', __name__)


class Production(db.Model, UserMixin):
    __tablename__ = 'production'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    production_name = db.Column(db.String(200))
    production_created_date = db.Column(db.Date)
    production_expected_date = db.Column(db.Date)
    team_id = db.Column(db.Integer, db.ForeignKey('production_team.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    production_state = db.Column(db.String(120))
    team = db.relationship("ProductionTeam")
    item = db.relationship("Items")
    production_line = db.relationship("ProductionLine", backref="production_line", lazy='dynamic')

    def __init__(self, team_id, production_created_date, production_state=None):
        self.production_created_date = production_created_date
        self.team_id = team_id
        self.production_state = production_state
        # self.active = active

    def __repr__(self):
        return self.production_name



