# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

sample_model_blueprint = Blueprint('sample_model_blueprint', __name__)

# initiating the class
class Sample(db.Model, UserMixin):
    __tablename__ = 'sample'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)




