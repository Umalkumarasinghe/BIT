from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify
from models.production import Production
from models.production_line import ProductionLine
from models.suppliers import Supplier
from models.purchase_order import PurchaseOrder
from models.purchase_order_line import PurchaseOrderLine
from models.production_teams import ProductionTeam
from models.items import Items
from models.reordering import Reordering
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.production_forms import ProductionForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

production_actions_controllers = Blueprint('production_actions_controllers', __name__)


@production_actions_controllers.route('/view_production', methods=["GET", "POST"])
# @login_required
def view_production():
    objects = Production.query.all()
    return render_template('production/production.html', objects=objects)


@production_actions_controllers.route('/create_production_view', methods=["GET", "POST"])
@login_required
def create_production_view():
    form = ProductionForm()

    form.team_id.choices = [(team.id, team.production_team_name) for team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]

    return render_template('production/production_create.html', form=form, type='create')


@production_actions_controllers.route('/create_production', methods=["GET", "POST"])
@login_required
def create_production():
    if request.method == 'POST':
        production_values = json.loads(request.form.get('values'))
        production_main_object = production_values.get('productionData')
        production_items = production_values.get('itemData')
        object = Production(team_id=production_main_object.get('team_id'),
                            production_created_date=production_main_object.get('production_created_date'),
                            production_state="Pending")
        db.session.add(object)
        db.session.flush()
        object.production_name = "PR" + str(('{0:05d}'.format(object.id)))
        db.session.commit()
        for item in production_items:
            item_obj = ProductionLine(demand_quantity=item.get('demand_quantity'), item_id=item.get('item_product_id'), production_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return jsonify(id=object.id)
        return redirect(url_for('production_actions_controllers.view_production'))
    # flash('Something went wrong.')
    return redirect(url_for('production_actions_controllers.create_production_view'))


@production_actions_controllers.route('/view_production_view', methods=["GET", "POST"])
@login_required
def view_production_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_object(id)
    return redirect(url_for('production_actions_controllers.view_production'))


def redirect_object(id):
    object = Production.query.filter_by(id=id).first()
    return render_template('production/production_create.html', form=ProductionForm(), type='view',
                           object=object)


@production_actions_controllers.route('/edit_production_view', methods=["GET", "POST"])
@login_required
def edit_production_view():
    form = ProductionForm()
    form.team_id.choices = [(team.id, team.production_team_name) for team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    id = int(request.values.get('id'))
    if id:
        object = Production.query.filter_by(id=id).first()
        items = ProductionLine.query.filter_by(production_id=id).all()
        form.item_product_id.default = object.item_id
        form.team_id.default = object.team_id
        form.process()
        return render_template('production/production_create.html', form=form, type='edit', object=object,
                               items=items)
    return redirect(url_for('production_actions_controllers.view_production'))


@production_actions_controllers.route('/edit_production', methods=["GET", "POST"])
@login_required
def edit_production():
    if request.method == 'POST':
        production_values = json.loads(request.form.get('values'))
        production_main_object = production_values.get('productionData')
        production_items = production_values.get('itemData')
        vals = {
            'team_id': production_main_object.get('team_id'),
            'production_created_date': production_main_object.get('production_created_date')
        }
        id = production_main_object.get('id')
        Production.query.filter(Production.id == id).update(vals)
        db.session.commit()
        for item in production_items:
            record = ProductionLine.query.filter_by(id=item.get('itemId')).first()
            record.demand_quantity = int(item.get('demand_quantity'))
            db.session.commit()
            record.item_product_id = item.get('item_product_id')
            db.session.commit()
        return jsonify(success="success")


def redirect_object(id):
    form = ProductionForm()
    form.team_id.choices = [(team.id, team.production_team_name) for team in Supplier.query.all()]
    form.item_product_id.choices = [(item.id, item.name) for item in Items.query.all()]
    object = Production.query.filter_by(id=id).first()
    form.item_product_id.default = object.item_id
    form.team_id.default = object.team_id
    return render_template('production/production_create.html', form=form, type='view', object=object)


@production_actions_controllers.route('/delete_production', methods=["GET", "POST"])
@login_required
def delete_production():
    id = int(request.values.get('id'))
    if id:
        db.session.query(ProductionLine).filter(ProductionLine.production_id == id).delete()
        db.session.commit()
        Production.query.filter(Production.id == id).delete()
        db.session.commit()
        return redirect(url_for('production_actions_controllers.view_production', _anchor="content", ))


@production_actions_controllers.route('/complete_production', methods=["GET", "POST"])
@login_required
def complete_production():
    if request.method == 'POST':
        production_values = json.loads(request.form.get('values'))
        production_main_object = production_values.get('productionData')
        production_items = production_values.get('itemData')
        id = production_main_object.get('id')
        vals = {
            'production_state': "Completed",
        }
        Production.query.filter(Production.id == id).update(vals)
        db.session.commit()
        for item in production_items:
            object = Items.query.filter_by(id=item.get('item_product_id')).first()
            object.item_quantity = object.item_quantity - int(item.get('demand_quantity'))
            db.session.commit()
            check_reordering(object, object.item_quantity)
        return jsonify(success="success")

def check_reordering(item, item_quantity):
    reorder = Reordering.query.filter(Reordering.item_id==item.id, Reordering.minimum_quantity >= item_quantity).first()
    if reorder:
        object = PurchaseOrder(supplier_id=reorder.supplier_id, purchase_order_created_date=datetime.now(),
                               purchase_order_state="Pending",
                               purchase_order_expected_date=datetime.now(),
                               reorder=True,
                               purchase_total=0)
        db.session.add(object)
        db.session.flush()
        object.purchase_order_name = "PO/" + str(('{0:05d}'.format(object.id)))
        db.session.commit()
        item_obj = PurchaseOrderLine(item_id=item.id, quantity=reorder.maximum_quantity - item_quantity,
                           unit_price=0, subtotal=0,
                           purchase_order_id=object.id)
        db.session.add(item_obj)
        db.session.commit()
        return True