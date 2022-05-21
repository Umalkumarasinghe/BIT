from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify
from models.production_order import ProductionOrder
from models.production_order_line import ProductionOrderLine
from models.production_teams import ProductionTeam
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.production_order_forms import ProductionOrderForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

production_order_actions_controllers = Blueprint('production_order_actions_controllers', __name__)


@production_order_actions_controllers.route('/view_production_order', methods=["GET", "POST"])
# @login_required
def view_production_order():
    objects = ProductionOrder.query.all()
    return render_template('production_order/production_order.html', objects=objects)


@production_order_actions_controllers.route('/create_production_order_view', methods=["GET", "POST"])
@login_required
def create_production_order_view():
    form = ProductionOrderForm()

    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]

    return render_template('production_order/production_order_create.html', form=form, type='create')


@production_order_actions_controllers.route('/create_production_order', methods=["GET", "POST"])
@login_required
def create_production_order():
    if request.method == 'POST':
        production_order_values = json.loads(request.form.get('values'))
        production_order_main_object = production_order_values.get('production_orderData')
        production_order_items = production_order_values.get('itemData')
        object = ProductionOrder(production_team_id=production_order_main_object.get('production_team_id'),
                               production_order_name=production_order_main_object.get('production_order_name'),
                               production_order_created_date=production_order_main_object.get(
                                   'production_order_created_date'),
                               production_order_expected_date=production_order_main_object.get(
                                   'production_order_expected_date'))
        db.session.add(object)
        db.session.commit()
        for item in production_order_items:
            item_obj = ProductionOrderLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('item_quantity_line'),
                                         item_id=item.get('item_product_id'), production_order_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return redirect(url_for('production_order_actions_controllers.view_production_order'))
    # flash('Something went wrong.')
    return redirect(url_for('production_order_actions_controllers.create_production_order_view'))


@production_order_actions_controllers.route('/view_production_order_view', methods=["GET", "POST"])
@login_required
def view_production_order_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_object(id)
    return redirect(url_for('production_order_actions_controllers.view_production_order'))


def redirect_object(id):
    object = ProductionOrder.query.filter_by(id=id).first()
    return render_template('production_order/production_order_create.html', form=ProductionOrderForm(), type='view',
                           object=object)


@production_order_actions_controllers.route('/edit_production_order_view', methods=["GET", "POST"])
@login_required
def edit_production_order_view():
    form = ProductionOrderForm()
    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    id = int(request.values.get('id'))
    if id:
        object = ProductionOrder.query.filter_by(id=id).first()
        items = ProductionOrderLine.query.filter_by(production_order_id=id).all()
        form.item_product_id.default = object.item_id
        form.production_team_id.default = object.production_team_id
        form.process()
        return render_template('production_order/production_order_create.html', form=form, type='edit', object=object,
                               items=items)
    return redirect(url_for('production_order_actions_controllers.view_production_order'))


@production_order_actions_controllers.route('/edit_production_order', methods=["GET", "POST"])
@login_required
def edit_production_order():
    if request.method == 'POST':
        production_order_values = json.loads(request.form.get('values'))
        production_order_main_object = production_order_values.get('production_orderData')
        production_order_items = production_order_values.get('itemData')
        vals = {
            'production_team_id': production_order_main_object.get('production_team_id'),
            'production_order_name': production_order_main_object.get('production_order_name'),
            'production_order_created_date': production_order_main_object.get('production_order_created_date'),
            'production_order_expected_date': production_order_main_object.get('production_order_expected_date'),
            'production_order_state': production_order_main_object.get('production_order_state')
        }
        id = production_order_main_object.get('id')
        ProductionOrder.query.filter(ProductionOrder.id == id).update(vals)
        db.session.commit()
        ProductionOrderLine.query.filter(ProductionOrderLine.production_order_id == id).delete()
        db.session.commit()
        for item in production_order_items:
            item_obj = ProductionOrderLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'),
                                         item_id=item.get('item_product_id'), production_order_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(id)
    flash('Something went wrong.')
    return redirect(url_for('production_order_actions_controllers.edit_production_order_view'))


@production_order_actions_controllers.route('/view_confirmed_production_order', methods=["GET", "POST"])
# @login_required
def view_confirmed_production_order():
    objects = ProductionOrder.query.filter_by(production_order_state='Confirmed')
    return render_template('production_order/production_order.html', objects=objects, type='confirmed_order_view')


@production_order_actions_controllers.route('/confirm_production_order', methods=["GET", "POST"])
@login_required
def confirm_production_order():
    if request.method == 'POST':
        production_order_values = json.loads(request.form.get('values'))
        production_order_main_object = production_order_values.get('production_orderData')
        production_order_items = production_order_values.get('itemData')
        vals = {
            'production_team_id': production_order_main_object.get('production_team_id'),
            'production_order_name': production_order_main_object.get('production_order_name'),
            'production_order_created_date': production_order_main_object.get('production_order_created_date'),
            'production_order_expected_date': production_order_main_object.get('production_order_expected_date'),
            'production_order_state': production_order_main_object.get('production_order_state')
        }
        id = production_order_main_object.get('id')
        ProductionOrder.query.filter(ProductionOrder.id == id).update(vals)
        db.session.commit()
        ProductionOrderLine.query.filter(ProductionOrderLine.production_order_id == id).delete()
        db.session.commit()
        for item in production_order_items:
            item_obj = ProductionOrderLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'),
                                         item_id=item.get('item_product_id'), production_order_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(url_for('production_order_actions_controllers.edit_production_order_view', type='view'))
    flash('Something went wrong.')
    return redirect(url_for('production_order_actions_controllers.edit_production_order_view'))


def redirect_object(id):
    form = ProductionOrderForm()
    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.name) for item in Items.query.all()]
    object = ProductionOrder.query.filter_by(id=id).first()
    form.item_product_id.default = object.item_id
    form.production_team_id.default = object.production_team_id
    return render_template('production_order/production_order_create.html', form=form, type='view', object=object)


@production_order_actions_controllers.route('/delete_production_order', methods=["GET", "POST"])
@login_required
def delete_production_order():
    id = int(request.values.get('id'))
    if id:
        # productionOrder.query.filter(productionOrder.id == id).delete()
        db.session.query(ProductionOrder).filter(ProductionOrder.id == id).delete()
        db.session.query(ProductionOrderLine).filter(ProductionOrderLine.id == id).delete()
        db.session.commit()

        return redirect(url_for('production_order_actions_controllers.view_production_order', _anchor="content", ))