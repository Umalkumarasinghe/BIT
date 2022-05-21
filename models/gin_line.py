from app import db
from flask import Blueprint
from flask_login import UserMixin

gin_line_model_blueprint = Blueprint('gin_line_model_blueprint', __name__)


class GinLine(db.Model, UserMixin):
    __tablename__ = 'gin_line'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name_line = db.Column(db.String(10))
    item_quantity_line = db.Column(db.Integer)
    item_sent_quantity_line = db.Column(db.Integer)
    description = db.Column(db.String(120), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship("Items")
    production_team_id = db.Column(db.Integer, db.ForeignKey('production_team.id'))
    production_team = db.relationship("ProductionTeam")
    gin_id = db.Column(db.Integer, db.ForeignKey('gin.id'))
    gin = db.relationship('Gin')

    def __init__(self, item_id, item_quantity_line, item_sent_quantity_line, item_name_line, gin_id):
        self.item_id = item_id
        self.item_quantity_line = item_quantity_line
        self.item_name_line = item_name_line
        self.item_sent_quantity_line = item_sent_quantity_line
        self.gin_id = gin_id

    def __repr__(self):
        return self.item_id



