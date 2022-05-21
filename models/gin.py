from app import db
from flask import Blueprint
from flask_login import UserMixin

gin_model_blueprint = Blueprint('gin_model_blueprint', __name__)


class Gin(db.Model, UserMixin):
    __tablename__ = 'gin'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    gin_name = db.Column(db.String(200))
    gin_created_date = db.Column(db.Date)
    gin_expected_date = db.Column(db.Date)
    production_team_id = db.Column(db.Integer, db.ForeignKey('production_team.id'))
    production_team = db.relationship("ProductionTeam")
    gin_state = db.Column(db.String(120))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    gin_line = db.relationship("GinLine", backref="gin_line", lazy='dynamic')


    def __init__(self,production_team_id, gin_name, gin_created_date, gin_expected_date, gin_state=None):
        self.gin_name = gin_name,
        self.gin_created_date = gin_created_date
        self.gin_expected_date = gin_expected_date
        self.production_team_id = production_team_id
        self.gin_state = gin_state
        # self.active = active

    def __repr__(self):
        return self.gin_name



