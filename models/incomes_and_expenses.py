# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

incomes_and_expenses_model_blueprint = Blueprint('incomes_and_expenses_model_blueprint', __name__)

# initiating the class
class IncomesAndExpenses(db.Model, UserMixin):
    __tablename__ = 'incomes_and_expenses'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Date)
    type = db.Column(db.String(120))
    category = db.Column(db.String(120))
    amount = db.Column(db.Integer)

    # init function
    def __init__(self, date, type, category, amount):

        self.date = date
        self.type = type
        self.category = category
        self.amount = amount

    # returns object in string format
    def __repr__(self):
        return self.date



