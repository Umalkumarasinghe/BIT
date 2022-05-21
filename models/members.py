# importing files and libraries
from app import db
from flask import Blueprint
from flask_login import UserMixin

member_model_blueprint = Blueprint('member_model_blueprint', __name__)

# initiating the class
class Member(db.Model, UserMixin):
    __tablename__ = 'member'

    # table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean)
    full_name = db.Column(db.String(200))
    calling_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer())
    gender = db.Column(db.String(10))
    nic = db.Column(db.String(12), unique=True)
    emergency_contact = db.Column(db.String(120))
    emergency_contact_relationship = db.Column(db.String(120))
    emergency_contact_no = db.Column(db.String(20))
    contact_no = db.Column(db.String(20))
    address = db.Column(db.String(255))

    # init function
    def __init__(self, email, full_name, calling_name, date_of_birth, age, gender, nic, emergency_contact, emergency_contact_relationship, emergency_contact_no, contact_no, address, active=None):
        self.email = email
        self.active = active
        self.full_name = full_name
        self.calling_name = calling_name
        self.date_of_birth = date_of_birth
        self.age = age
        self.gender = gender
        self.nic = nic
        self.emergency_contact = emergency_contact
        self.emergency_contact_relationship = emergency_contact_relationship
        self.emergency_contact_no = emergency_contact_no
        self.contact_no = contact_no
        self.address = address

    # returns object in string format
    def __repr__(self):
        return self.calling_name



