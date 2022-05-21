# importing libraries and files
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from models.production_teams import ProductionTeam
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.production_team_forms import CreateProductionTeamForm
import json
from datetime import datetime

production_team_actions_controller = Blueprint('production_team_actions_controller', __name__)

# view all production_team list
@production_team_actions_controller.route('/view_production_teams', methods=["GET", "POST"])
@login_required
def view_production_teams():
    production_teams = ProductionTeam.query.all()
    return render_template('production_teams/production_teams.html', production_teams=production_teams)


# load member create view
@production_team_actions_controller.route('/create_production_teams_view', methods=["GET", "POST"])
@login_required
def create_production_teams_view():
    return render_template('production_teams/production_teams_create.html', form=CreateProductionTeamForm(), type='create')


# create member when form is submitted
@production_team_actions_controller.route('/create_production_team', methods=["GET", "POST"])
@login_required
def create_production_team():
    create_production_team_from = CreateProductionTeamForm(request.form)
    if request.method == 'POST':
        if create_production_team_from.validate():
            production_team_name = request.form['production_team_name']
            production_team_email = request.form['production_team_email']
            production_team_contact_no = request.form['production_team_contact_no']
            production_team_address = request.form['production_team_address']

            existing_member = ProductionTeam.query.filter(or_(ProductionTeam.production_team_name == production_team_name, ProductionTeam.production_team_email==production_team_email)).first()
            if not existing_member:
                production_team = ProductionTeam(production_team_name=production_team_name, production_team_email=production_team_email, production_team_contact_no=production_team_contact_no, production_team_address=production_team_address)
                db.session.add(production_team)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('production_team_actions_controller.view_production_teams'))
        flash('A production_team already exists with the Email address/ Name')
    return redirect(url_for('production_team_actions_controller.create_production_teams_view'))


# load created member with form view
@production_team_actions_controller.route('/view_production_team_view', methods=["GET", "POST"])
@login_required
def view_production_team_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_production_team(id)
    return redirect(url_for('production_team_actions_controller.view_production_teams'))


# normal function
def redirect_production_team(id):
    production_team = ProductionTeam.query.filter_by(id=id).first()
    return render_template('production_teams/production_teams_create.html', form=CreateProductionTeamForm(), type='view', production_team=production_team)


# load member edit view
@production_team_actions_controller.route('/edit_production_team_view', methods=["GET", "POST"])
@login_required
def edit_production_team_view():
    id = int(request.values.get('id'))
    if id:
        production_team = ProductionTeam.query.filter_by(id=id).first()
        return render_template('production_teams/production_teams_create.html', form=CreateProductionTeamForm(), type='edit', production_team=production_team)
    return redirect(url_for('production_team_actions_controller.view_production_teams'))


# edit member when form is submitted
@production_team_actions_controller.route('/edit_production_team', methods=["GET", "POST"])
@login_required
def edit_production_team():
    if request.method == 'POST':
        vals = {
            'production_team_name': request.form['production_team_name'],
            'production_team_email': request.form['production_team_email'],
            'production_team_contact_no': request.form['production_team_contact_no'],
            'production_team_address': request.form['production_team_address'],
        }
        id = request.form['id']
        existing_production_team = ProductionTeam.query.filter(or_(ProductionTeam.production_team_email==request.form['production_team_email'])).all()
        if existing_production_team:
            ProductionTeam.query.filter(ProductionTeam.id==id).update(vals)
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect_production_team(id)
    flash('A member already exists with the Email address')
    return redirect(url_for('production_team_actions_controller.edit_production_team_view'))

@production_team_actions_controller.route('/delete_production_team', methods=["GET", "POST"])
@login_required
def delete_production_team():

    id = int(request.values.get('id'))
    if id:
        ProductionTeam.query.filter(ProductionTeam.id==id).delete()
        db.session.commit()
        return redirect(url_for('production_team_actions_controller.view_production_teams', _anchor="content", ))