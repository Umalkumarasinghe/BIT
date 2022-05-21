from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify
from models.purchase_order import PurchaseOrder
from models.purchase_order_line import PurchaseOrderLine
from models.suppliers import Supplier
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.purchase_order_forms import PurchaseOrderForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

purchase_order_actions_controllers = Blueprint('purchase_order_actions_controllers', __name__)


@purchase_order_actions_controllers.route('/view_purchase_order', methods=["GET", "POST"])
# @login_required
def view_purchase_order():
    objects = PurchaseOrder.query.all()
    return render_template('purchase_order/purchase_order.html', objects=objects)


@purchase_order_actions_controllers.route('/create_purchase_order_view', methods=["GET", "POST"])
@login_required
def create_purchase_order_view():
    form = PurchaseOrderForm()
    
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    
    return render_template('purchase_order/purchase_order_create.html', form=form, type='create')


@purchase_order_actions_controllers.route('/get_unit_price', methods=["GET", "POST"])
def get_unit_price():
    package_id = request.form.get('item_product_id')
    object = Items.query.filter_by(id=int(package_id)).first()
    return jsonify(price=object.item_unit_price)


@purchase_order_actions_controllers.route('/create_purchase_order', methods=["GET", "POST"])
@login_required
def create_purchase_order():
    if request.method == 'POST':
        purchase_order_values = json.loads(request.form.get('values'))
        purchase_order_main_object = purchase_order_values.get('purchase_orderData')
        purchase_order_items = purchase_order_values.get('itemData')
        object = PurchaseOrder(purchase_order_state="Pending",
                               supplier_id=purchase_order_main_object.get('supplier_id'),
                               purchase_total=purchase_order_main_object.get('purchase_total'),
                               purchase_order_name=purchase_order_main_object.get('name'),
                               purchase_order_created_date=purchase_order_main_object.get('purchase_order_created_date'),
                               purchase_order_expected_date=purchase_order_main_object.get('purchase_order_expected_date'))
        db.session.add(object)
        db.session.commit()
        for item in purchase_order_items:
            item_obj = PurchaseOrderLine(quantity=item.get('quantity'), subtotal=item.get('subtotal'), unit_price=item.get('unit_price'), item_id=item.get('item_product_id'), purchase_order_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return redirect(url_for('purchase_order_actions_controllers.view_purchase_order'))
    # flash('Something went wrong.')
    return redirect(url_for('purchase_order_actions_controllers.create_purchase_order_view'))


@purchase_order_actions_controllers.route('/view_purchase_order_view', methods=["GET", "POST"])
@login_required
def view_purchase_order_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_object(id)
    return redirect(url_for('purchase_order_actions_controllers.view_purchase_order'))


def redirect_object(id):
    object = PurchaseOrder.query.filter_by(id=id).first()
    return render_template('purchase_order/purchase_order_create.html', form=PurchaseOrderForm(), type='view', object=object)


@purchase_order_actions_controllers.route('/edit_purchase_order_view', methods=["GET", "POST"])
@login_required
def edit_purchase_order_view():
    form = PurchaseOrderForm()
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    id = int(request.values.get('id'))
    if id:
        object = PurchaseOrder.query.filter_by(id=id).first()
        items = PurchaseOrderLine.query.filter_by(purchase_order_id=id).all()
        form.item_product_id.default = object.item_id
        form.supplier_id.default = object.supplier_id
        form.process()
        return render_template('purchase_order/purchase_order_create.html', form=form, type='edit', object=object, items=items)
    return redirect(url_for('purchase_order_actions_controllers.view_purchase_order'))


@purchase_order_actions_controllers.route('/edit_purchase_order', methods=["GET", "POST"])
@login_required
def edit_purchase_order():
    if request.method == 'POST':
        purchase_order_values = json.loads(request.form.get('values'))
        purchase_order_main_object = purchase_order_values.get('purchase_orderData')
        purchase_order_items = purchase_order_values.get('itemData')
        vals = {
            'supplier_id': purchase_order_main_object.get('supplier_id'),
            'purchase_order_name': purchase_order_main_object.get('purchase_order_name'),
            'purchase_order_created_date': purchase_order_main_object.get('purchase_order_created_date'),
            'purchase_order_expected_date': purchase_order_main_object.get('purchase_order_expected_date'),
            'purchase_order_state': purchase_order_main_object.get('purchase_order_state')
        }
        id = purchase_order_main_object.get('id')
        PurchaseOrder.query.filter(PurchaseOrder.id==id).update(vals)
        db.session.commit()
        PurchaseOrderLine.query.filter(PurchaseOrderLine.purchase_order_id==id).delete()
        db.session.commit()
        for item in purchase_order_items:
            item_obj = PurchaseOrderLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'),
                                         item_id=item.get('item_product_id'), purchase_order_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(id)
    flash('Something went wrong.')
    return redirect(url_for('purchase_order_actions_controllers.edit_purchase_order_view'))


@purchase_order_actions_controllers.route('/view_confirmed_purchase_order', methods=["GET", "POST"])
# @login_required
def view_confirmed_purchase_order():
    objects = PurchaseOrder.query.filter_by(purchase_order_state='Confirmed')
    return render_template('purchase_order/purchase_order.html', objects=objects, type='confirmed_order_view')


@purchase_order_actions_controllers.route('/confirm_purchase_order', methods=["GET", "POST"])
@login_required
def confirm_purchase_order():
    if request.method == 'POST':
        po_id = request.form.get('po_id')
        vals = {
            'purchase_order_state': "Confirmed",
        }
        PurchaseOrder.query.filter(PurchaseOrder.id == po_id).update(vals)
        db.session.commit()
        return redirect_object(url_for('purchase_order_actions_controllers.edit_purchase_order_view', type='view'))
    flash('Something went wrong.')
    return redirect(url_for('purchase_order_actions_controllers.edit_purchase_order_view'))


@purchase_order_actions_controllers.route('/create_grn', methods=["GET", "POST"])
@login_required
def create_grn():
    if request.method == 'POST':
        purchase_order_values = json.loads(request.form.get('values'))
        purchase_order_main_object = purchase_order_values.get('purchase_orderData')
        purchase_order_items = purchase_order_values.get('itemData')
        vals = {
            'supplier_id': purchase_order_main_object.get('supplier_id'),
            'purchase_order_name': purchase_order_main_object.get('purchase_order_name'),
            'purchase_order_created_date': purchase_order_main_object.get('purchase_order_created_date'),
            'purchase_order_expected_date': purchase_order_main_object.get('purchase_order_expected_date'),
            'purchase_order_state': purchase_order_main_object.get('purchase_order_state')
        }
        id = purchase_order_main_object.get('id')
        PurchaseOrder.query.filter(PurchaseOrder.id==id).update(vals)
        db.session.commit()
        PurchaseOrderLine.query.filter(PurchaseOrderLine.purchase_order_id==id).delete()
        db.session.commit()
        for item in purchase_order_items:
            item_obj = PurchaseOrderLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'),
                                         item_id=item.get('item_product_id'), purchase_order_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(url_for('purchase_order_actions_controllers.edit_purchase_order_view', type='view'))
    flash('Something went wrong.')
    return redirect(url_for('purchase_order_actions_controllers.edit_purchase_order_view'))


def redirect_object(id):
    form = PurchaseOrderForm()
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name) for supplier in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.name) for item in Items.query.all()]
    object = PurchaseOrder.query.filter_by(id=id).first()
    form.item_product_id.default = object.item_id
    form.supplier_id.default = object.supplier_id
    return render_template('purchase_order/purchase_order_create.html', form=form, type='view', object=object)


@purchase_order_actions_controllers.route('/delete_purchase_order', methods=["GET", "POST"])
@login_required
def delete_purchase_order():
    id = int(request.values.get('id'))
    if id:
        #PurchaseOrder.query.filter(PurchaseOrder.id == id).delete()
        db.session.query(PurchaseOrder).filter(PurchaseOrder.id == id).delete()
        db.session.query(PurchaseOrderLine).filter(PurchaseOrderLine.id == id).delete()
        db.session.commit()
        return redirect(url_for('purchase_order_actions_controllers.view_purchase_order', _anchor="content", ))