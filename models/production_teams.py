# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

production_team_model_blueprint = Blueprint('production_team_model_blueprint', __name__)

# initiating the class
class ProductionTeam(db.Model, UserMixin):
    __tablename__ = 'production_team'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    production_team_name = db.Column(db.String(200))
    production_team_email = db.Column(db.String(120), unique=True)
    production_team_contact_no = db.Column(db.String(20))
    production_team_address = db.Column(db.String(255))

    # init function
    def __init__(self, production_team_name, production_team_email, production_team_contact_no, production_team_address):

        self.production_team_name = production_team_name
        self.production_team_email = production_team_email
        self.production_team_contact_no = production_team_contact_no
        self.production_team_address = production_team_address

    # returns object in string format
    def __repr__(self):
        return self.production_team_name



