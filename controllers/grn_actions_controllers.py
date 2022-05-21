from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify
from models.grn import Grn
from models.grn_line import GrnLine
from models.suppliers import Supplier
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.grn_forms import GrnForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

grn_actions_controllers = Blueprint('grn_actions_controllers', __name__)


@grn_actions_controllers.route('/view_grn', methods=["GET", "POST"])
# @login_required
def view_grn():
    objects = Grn.query.all()
    return render_template('grn/grn.html', objects=objects)


@grn_actions_controllers.route('/create_grn_view', methods=["GET", "POST"])
@login_required
def create_grn_view():
    form = GrnForm()

    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]

    return render_template('grn/grn_create.html', form=form, type='create')


@grn_actions_controllers.route('/create_grn', methods=["GET", "POST"])
@login_required
def create_grn():
    if request.method == 'POST':
        grn_values = json.loads(request.form.get('values'))
        grn_main_object = grn_values.get('grnData')
        grn_items = grn_values.get('itemData')
        object = Grn(supplier_id=grn_main_object.get('supplier_id'),
                               grn_name=grn_main_object.get('grn_name'),
                               grn_created_date=grn_main_object.get(
                                   'grn_created_date'),
                               grn_expected_date=grn_main_object.get(
                                   'grn_expected_date'))
        db.session.add(object)
        db.session.commit()
        for item in grn_items:
            item_obj = GrnLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('item_quantity_line'), received_quantity_line=item.get('received_quantity'),
                                         item_id=item.get('item_product_id'), grn_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return redirect(url_for('grn_actions_controllers.view_grn'))
    # flash('Something went wrong.')
    return redirect(url_for('grn_actions_controllers.create_grn_view'))


@grn_actions_controllers.route('/view_grn_view', methods=["GET", "POST"])
@login_required
def view_grn_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_object(id)
    return redirect(url_for('grn_actions_controllers.view_grn'))


def redirect_object(id):
    object = Grn.query.filter_by(id=id).first()
    return render_template('grn/grn_create.html', form=GrnForm(), type='view',
                           object=object)


@grn_actions_controllers.route('/edit_grn_view', methods=["GET", "POST"])
@login_required
def edit_grn_view():
    form = GrnForm()
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    id = int(request.values.get('id'))
    if id:
        object = Grn.query.filter_by(id=id).first()
        items = GrnLine.query.filter_by(grn_id=id).all()
        form.item_product_id.default = object.item_id
        form.supplier_id.default = object.supplier_id
        form.process()
        return render_template('grn/grn_create.html', form=form, type='edit', object=object,
                               items=items)
    return redirect(url_for('grn_actions_controllers.view_grn'))


@grn_actions_controllers.route('/edit_grn', methods=["GET", "POST"])
@login_required
def edit_grn():
    if request.method == 'POST':
        grn_values = json.loads(request.form.get('values'))
        grn_main_object = grn_values.get('grnData')
        grn_items = grn_values.get('itemData')
        vals = {
            'supplier_id': grn_main_object.get('supplier_id'),
            'grn_name': grn_main_object.get('grn_name'),
            'grn_created_date': grn_main_object.get('grn_created_date'),
            'grn_expected_date': grn_main_object.get('grn_expected_date'),
            'grn_state': grn_main_object.get('grn_state')
        }
        id = grn_main_object.get('id')
        Grn.query.filter(Grn.id == id).update(vals)
        db.session.commit()
        GrnLine.query.filter(GrnLine.grn_id == id).delete()
        db.session.commit()
        for item in grn_items:
            item_obj = GrnLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'), received_quantity_line=item.get('received_quantity'), item_id=item.get('item_product_id'), grn_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(id)
    flash('Something went wrong.')
    return redirect(url_for('grn_actions_controllers.edit_grn_view'))


def redirect_object(id):
    form = GrnForm()
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.name) for item in Items.query.all()]
    object = Grn.query.filter_by(id=id).first()
    form.item_product_id.default = object.item_id
    form.supplier_id.default = object.supplier_id
    return render_template('grn/grn_create.html', form=form, type='view', object=object)


@grn_actions_controllers.route('/delete_grn', methods=["GET", "POST"])
@login_required
def delete_grn():
    id = int(request.values.get('id'))
    if id:
        # Grn.query.filter(Grn.id == id).delete()
        db.session.query(Grn).filter(Grn.id == id).delete()
        db.session.query(GrnLine).filter(GrnLine.id == id).delete()
        db.session.commit()

        return redirect(url_for('grn_actions_controllers.view_grn', _anchor="content", ))