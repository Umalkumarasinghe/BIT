from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify
from models.gin import Gin
from models.gin_line import GinLine
from models.production_teams import ProductionTeam
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.gin_forms import GinForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

gin_actions_controllers = Blueprint('gin_actions_controllers', __name__)


@gin_actions_controllers.route('/view_gin', methods=["GET", "POST"])
# @login_required
def view_gin():
    objects = Gin.query.all()
    return render_template('gin/gin.html', objects=objects)


@gin_actions_controllers.route('/create_gin_view', methods=["GET", "POST"])
@login_required
def create_gin_view():
    form = GinForm()

    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]

    return render_template('gin/gin_create.html', form=form, type='create')


@gin_actions_controllers.route('/create_gin', methods=["GET", "POST"])
@login_required
def create_gin():
    if request.method == 'POST':
        gin_values = json.loads(request.form.get('values'))
        gin_main_object = gin_values.get('ginData')
        gin_items = gin_values.get('itemData')
        object = Gin(production_team_id=gin_main_object.get('production_team_id'),
                               gin_name=gin_main_object.get('gin_name'),
                               gin_created_date=gin_main_object.get(
                                   'gin_created_date'),
                               gin_expected_date=gin_main_object.get(
                                   'gin_expected_date'))
        db.session.add(object)
        db.session.commit()
        for item in gin_items:
            item_obj = GinLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('item_quantity_line'), sent_quantity_line=item.get('sent_quantity'),
                                         item_id=item.get('item_product_id'), gin_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return redirect(url_for('gin_actions_controllers.view_gin'))
    # flash('Something went wrong.')
    return redirect(url_for('gin_actions_controllers.create_gin_view'))


@gin_actions_controllers.route('/view_gin_view', methods=["GET", "POST"])
@login_required
def view_gin_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_object(id)
    return redirect(url_for('gin_actions_controllers.view_gin'))


def redirect_object(id):
    object = Gin.query.filter_by(id=id).first()
    return render_template('gin/gin_create.html', form=GinForm(), type='view',
                           object=object)


@gin_actions_controllers.route('/edit_gin_view', methods=["GET", "POST"])
@login_required
def edit_gin_view():
    form = GinForm()
    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.item_name) for item in Items.query.all()]
    id = int(request.values.get('id'))
    if id:
        object = Gin.query.filter_by(id=id).first()
        items = GinLine.query.filter_by(gin_id=id).all()
        form.item_product_id.default = object.item_id
        form.production_team_id.default = object.production_team_id
        form.process()
        return render_template('gin/gin_create.html', form=form, type='edit', object=object,
                               items=items)
    return redirect(url_for('gin_actions_controllers.view_gin'))


@gin_actions_controllers.route('/edit_gin', methods=["GET", "POST"])
@login_required
def edit_gin():
    if request.method == 'POST':
        gin_values = json.loads(request.form.get('values'))
        gin_main_object = gin_values.get('ginData')
        gin_items = gin_values.get('itemData')
        vals = {
            'production_team_id': gin_main_object.get('production_team_id'),
            'gin_name': gin_main_object.get('gin_name'),
            'gin_created_date': gin_main_object.get('gin_created_date'),
            'gin_expected_date': gin_main_object.get('gin_expected_date'),
            'gin_state': gin_main_object.get('gin_state')
        }
        id = gin_main_object.get('id')
        Gin.query.filter(Gin.id == id).update(vals)
        db.session.commit()
        GinLine.query.filter(GinLine.gin_id == id).delete()
        db.session.commit()
        for item in gin_items:
            item_obj = GinLine(item_name_line=item.get('item_name_line'),
                                         item_quantity_line=item.get('quantity'), sent_quantity_line=item.get('sent_quantity'), item_id=item.get('item_product_id'), gin_id=id)
            db.session.add(item_obj)
            db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_object(id)
    flash('Something went wrong.')
    return redirect(url_for('gin_actions_controllers.edit_gin_view'))


def redirect_object(id):
    form = GinForm()
    form.production_team_id.choices = [(production_team.id, production_team.production_team_name) for production_team in ProductionTeam.query.all()]
    form.item_product_id.choices = [(item.id, item.name) for item in Items.query.all()]
    object = Gin.query.filter_by(id=id).first()
    form.item_product_id.default = object.item_id
    form.production_team_id.default = object.production_team_id
    return render_template('gin/gin_create.html', form=form, type='view', object=object)


@gin_actions_controllers.route('/delete_gin', methods=["GET", "POST"])
@login_required
def delete_gin():
    id = int(request.values.get('id'))
    if id:
        # Gin.query.filter(Gin.id == id).delete()
        db.session.query(Gin).filter(Gin.id == id).delete()
        db.session.query(GinLine).filter(GinLine.id == id).delete()
        db.session.commit()

        return redirect(url_for('gin_actions_controllers.view_gin', _anchor="content", ))