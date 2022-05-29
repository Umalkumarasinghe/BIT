# importing libraries and files
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, send_file
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.item_form import CreateItemForm
import json
from datetime import datetime
import xlsxwriter

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


# edit member when form is submitted
@item_actions_controller.route('/inventory_report', methods=["GET", "POST"])
@login_required
def inventory_report():
    report = 'Inventory Report' + '.xlsx'
    workbook = xlsxwriter.Workbook(report)

    # Create worksheet 1
    worksheet = workbook.add_worksheet('Inventory Report')
    worksheet.set_landscape()

    heading = workbook.add_format({'bold': True, 'align': 'center', 'font_size': '14'})
    heading_2 = workbook.add_format({'bold': True, 'align': 'left', 'font_size': '12'})
    font_right = workbook.add_format(
        {'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'num_format': '#,##0.00', 'border': 1})
    font_left = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'font_size': 10, 'num_format': '#,##0.00', 'border': 1})
    font_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 10, 'border': 1})
    font_center_bold = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'font_size': 10, 'bold': True, 'border': 1})
    font_right_bold = workbook.add_format(
        {'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'num_format': '#,##0.00', 'bold': True})
    font_left_bold = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'font_size': 10, 'num_format': '#,##0.00', 'bold': True})

    worksheet.set_column('A:S', 20)
    worksheet.set_row(0, 20)

    row = 0
    col = 0

    # Write data on the worksheet
    worksheet.write(row, col, " ", heading)
    worksheet.merge_range(row, col, row, col + 4, "Inventory Report", heading)

    col = 0
    row = 3

    worksheet.write(row, col, "Product", font_center_bold)
    worksheet.write(row, col + 1, "Code", font_center_bold)
    worksheet.write(row, col + 2, "Quantity", font_center_bold)
    worksheet.write(row, col + 3, "Unit Price", font_center_bold)

    row += 1

    for item in Items.query.filter_by().all():
        worksheet.write(row, col, item.item_name, font_left)
        worksheet.write(row, col + 1, item.item_code, font_left)
        worksheet.write(row, col + 2, item.item_quantity, font_left)
        worksheet.write(row, col + 3, item.item_unit_price, font_left)
        row += 1

    row += 1
    workbook.close()
    return send_file(report, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')