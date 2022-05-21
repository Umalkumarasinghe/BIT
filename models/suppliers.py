# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

supplier_model_blueprint = Blueprint('supplier_model_blueprint', __name__)

# initiating the class
class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    supplier_name = db.Column(db.String(200))
    supplier_email = db.Column(db.String(120), unique=True)
    supplier_contact_no = db.Column(db.String(20))
    supplier_address = db.Column(db.String(255))

    # init function
    def __init__(self, supplier_name, supplier_email, supplier_contact_no, supplier_address):

        self.supplier_name = supplier_name
        self.supplier_email = supplier_email
        self.supplier_contact_no = supplier_contact_no
        self.supplier_address = supplier_address

    # returns object in string format
    def __repr__(self):
        return self.supplier_name



