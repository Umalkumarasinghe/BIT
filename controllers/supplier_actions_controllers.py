# importing libraries and files
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from models.suppliers import Supplier
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.supplier_form import CreateSupplierForm
import json
from datetime import datetime

supplier_actions_controller = Blueprint('supplier_actions_controller', __name__)

# view all supplier list
@supplier_actions_controller.route('/view_suppliers', methods=["GET", "POST"])
@login_required
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers/suppliers.html', suppliers=suppliers)


# load member create view
@supplier_actions_controller.route('/create_suppliers_view', methods=["GET", "POST"])
@login_required
def create_suppliers_view():
    return render_template('suppliers/suppliers_create.html', form=CreateSupplierForm(), type='create')


# create member when form is submitted
@supplier_actions_controller.route('/create_supplier', methods=["GET", "POST"])
@login_required
def create_supplier():
    create_supplier_from = CreateSupplierForm(request.form)
    if request.method == 'POST':
        if create_supplier_from.validate():
            supplier_name = request.form['supplier_name']
            supplier_email = request.form['supplier_email']
            supplier_contact_no = request.form['supplier_contact_no']
            supplier_address = request.form['supplier_address']

            existing_member = Supplier.query.filter(or_(Supplier.supplier_name == supplier_name, Supplier.supplier_email==supplier_email)).first()
            if not existing_member:
                supplier = Supplier(supplier_name=supplier_name, supplier_email=supplier_email, supplier_contact_no=supplier_contact_no, supplier_address=supplier_address)
                db.session.add(supplier)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('supplier_actions_controller.view_suppliers'))
        flash('A supplier already exists with the Email address/ Name')
    return redirect(url_for('supplier_actions_controller.create_suppliers_view'))


# load created member with form view
@supplier_actions_controller.route('/view_supplier_view', methods=["GET", "POST"])
@login_required
def view_supplier_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_supplier(id)
    return redirect(url_for('supplier_actions_controller.view_suppliers'))


# normal function
def redirect_supplier(id):
    supplier = Supplier.query.filter_by(id=id).first()
    return render_template('suppliers/suppliers_create.html', form=CreateSupplierForm(), type='view', supplier=supplier)


# load member edit view
@supplier_actions_controller.route('/edit_supplier_view', methods=["GET", "POST"])
@login_required
def edit_supplier_view():
    id = int(request.values.get('id'))
    if id:
        supplier = Supplier.query.filter_by(id=id).first()
        return render_template('suppliers/suppliers_create.html', form=CreateSupplierForm(), type='edit', supplier=supplier)
    return redirect(url_for('supplier_actions_controller.view_suppliers'))


# edit member when form is submitted
@supplier_actions_controller.route('/edit_supplier', methods=["GET", "POST"])
@login_required
def edit_supplier():
    if request.method == 'POST':
        vals = {
            'supplier_name': request.form['supplier_name'],
            'supplier_email': request.form['supplier_email'],
            'supplier_contact_no': request.form['supplier_contact_no'],
            'supplier_address': request.form['supplier_address'],
        }
        id = request.form['id']
        existing_supplier = Supplier.query.filter(or_(Supplier.supplier_email==request.form['supplier_email'])).all()
        if existing_supplier:
            Supplier.query.filter(Supplier.id==id).update(vals)
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect_supplier(id)
    flash('A member already exists with the Email address')
    return redirect(url_for('supplier_actions_controller.edit_supplier_view'))

@supplier_actions_controller.route('/delete_supplier', methods=["GET", "POST"])
@login_required
def delete_supplier():

    id = int(request.values.get('id'))
    if id:
        Supplier.query.filter(Supplier.id==id).delete()
        db.session.commit()
        return redirect(url_for('supplier_actions_controller.view_suppliers', _anchor="content", ))