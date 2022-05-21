# importing libraries and files
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from models.members import Member
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.member_forms import CreateMemberForm
import json
from datetime import datetime

member_actions_controller = Blueprint('member_actions_controller', __name__)


# view all members list
@member_actions_controller.route('/view_members', methods=["GET", "POST"])
# @login_required
def view_members():
    members = Member.query.all()
    return render_template('members/members.html', members=members)


# load member create view
@member_actions_controller.route('/create_members_view', methods=["GET", "POST"])
@login_required
def create_members_view():
    return render_template('members/members_create.html', form=CreateMemberForm(), type='create')


# create member when form is submitted
@member_actions_controller.route('/create_member', methods=["GET", "POST"])
@login_required
def create_member():
    create_member_from = CreateMemberForm(request.form)
    if request.method == 'POST':
        if create_member_from.validate():
            email = request.form['email']
            full_name = request.form['full_name']
            active = False
            calling_name = request.form['calling_name']
            date_of_birth = request.form['date_of_birth']
            age = request.form['age']
            gender = request.form['gender']
            nic = request.form['nic_no']
            emergency_contact = request.form['emergency_contact']
            emergency_contact_relationship = request.form['emergency_contact_relationship']
            emergency_contact_no = request.form['emergency_contact_no']
            contact_no = request.form['contact_no']
            address = request.form['address']
            existing_member = Member.query.filter(or_(Member.nic == nic, Member.email==email)).first()
            if not existing_member:
                member = Member(email=email, full_name=full_name, active=active, calling_name=calling_name, date_of_birth=date_of_birth, age=age, gender=gender, nic=nic,  emergency_contact=emergency_contact, emergency_contact_no=emergency_contact_no, emergency_contact_relationship=emergency_contact_relationship, contact_no=contact_no, address=address)
                db.session.add(member)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('member_actions_controller.view_members'))
        flash('A member already exists with the NIC/Email address')
    return redirect(url_for('member_actions_controller.create_members_view'))


# load created member with form view
@member_actions_controller.route('/view_member_view', methods=["GET", "POST"])
@login_required
def view_member_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_member(id)
    return redirect(url_for('member_actions_controller.view_members'))


# normal function
def redirect_member(id):
    member = Member.query.filter_by(id=id).first()
    return render_template('members/members_create.html', form=CreateMemberForm(), type='view', member=member)


# load member edit view
@member_actions_controller.route('/edit_member_view', methods=["GET", "POST"])
@login_required
def edit_member_view():
    id = current_user.id
    if id:
        member = Member.query.filter_by(id=id).first()
        return render_template('members/members_create.html', form=CreateMemberForm(), type='edit', member=member)
    return redirect(url_for('member_actions_controllers.view_members'))


# edit member when form is submitted
@member_actions_controller.route('/edit_member', methods=["GET", "POST"])
@login_required
def edit_member():
    if request.method == 'POST':
        vals = {
            'email': request.form['email'],
            'full_name': request.form['full_name'],
            'calling_name': request.form['calling_name'],
            'date_of_birth': request.form['date_of_birth'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'nic': request.form['nic_no'],
            'emergency_contact': request.form['emergency_contact'],
            'emergency_contact_relationship': request.form['emergency_contact_relationship'],
            'emergency_contact_no': request.form['emergency_contact_no'],
            'contact_no': request.form['contact_no'],
            'address': request.form['address'],
        }
        id = request.form['id']
        existing_member = Member.query.filter(or_(Member.email==request.form['email'])).all()
        if existing_member:
            Member.query.filter(Member.id==id).update(vals)
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect_member(id)
    flash('A member already exists with the NIC/Email address')
    return redirect(url_for('member_actions_controller.edit_member_view'))

