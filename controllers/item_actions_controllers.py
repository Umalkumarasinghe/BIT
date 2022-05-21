# importing libraries and files
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.item_form import CreateItemForm
import json
from datetime import datetime

item_actions_controller = Blueprint('item_actions_controller', __name__)

# view all supplier list
@item_actions_controller.route('/view_items', methods=["GET", "POST"])
@login_required
def view_items():
    items = Items.query.all()
    return render_template('items/items.html', items=items)


# load Items create view
@item_actions_controller.route('/create_items_view', methods=["GET", "POST"])
@login_required
def create_items_view():
    return render_template('items/items_create.html', form=CreateItemForm(), type='create')


# create item when form is submitted
@item_actions_controller.route('/create_item', methods=["GET", "POST"])
@login_required
def create_item():
    create_item_from = CreateItemForm(request.form)
    if request.method == 'POST':
        if create_item_from.validate():
            item_name = request.form['item_name']
            item_code = request.form['item_code']
            item_quantity = request.form['item_quantity']
            item_unit_price = request.form['item_unit_price']

            existing_item = Items.query.filter(or_(Items.item_name == item_name, Items.item_code==item_code)).first()
            if not existing_item:
                item = Items(item_name=item_name, item_code=item_code, item_quantity=item_quantity, item_unit_price=item_unit_price)
                db.session.add(item)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('item_actions_controller.view_items'))
        flash('A item already exists')
    return redirect(url_for('item_actions_controller.create_items_view'))


# load created item with form view
@item_actions_controller.route('/view_item_view', methods=["GET", "POST"])
@login_required
def view_item_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_item(id)
    return redirect(url_for('item_actions_controller.view_items'))


# normal function
def redirect_item(id):
    item = Items.query.filter_by(id=id).first()
    return render_template('items/items_create.html', form=CreateItemForm(), type='view', item=item)


# load member edit view
@item_actions_controller.route('/edit_item_view', methods=["GET", "POST"])
@login_required
def edit_item_view():
    id = int(request.values.get('id'))
    if id:
        item = Items.query.filter_by(id=id).first()
        return render_template('items/items_create.html', form=CreateItemForm(), type='edit', item=item)
    return redirect(url_for('item_actions_controller.view_items'))


# edit member when form is submitted
@item_actions_controller.route('/edit_item', methods=["GET", "POST"])
@login_required
def edit_item():
    if request.method == 'POST':
        vals = {
            'item_name': request.form['item_name'],
            'item_code': request.form['item_code'],
            'item_quantity': request.form['item_quantity'],
            'item_unit_price': request.form['item_unit_price'],
        }
        id = request.form['id']
        existing_item = Items.query.filter(or_(Items.item_name==request.form['item_name'])).all()
        if existing_item:
            Items.query.filter(Items.id==id).update(vals)
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect_item(id)
    flash('An Items already exists')
    return redirect(url_for('item_actions_controller.edit_item_view'))

@item_actions_controller.route('/delete_item', methods=["GET", "POST"])
@login_required
def delete_item():

    id = int(request.values.get('id'))
    if id:
        Items.query.filter(Items.id==id).delete()
        db.session.commit()
        return redirect(url_for('item_actions_controller.view_items', _anchor="content", ))