from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, jsonify, send_from_directory
from models.purchase_order import PurchaseOrder
from models.purchase_order_line import PurchaseOrderLine
from models.suppliers import Supplier
from models.grn import Grn
from models.grn_line import GrnLine
from models.items import Items
from models.users import User
from flask_login import login_required, current_user
from app import db
from sqlalchemy import or_
from forms.purchase_order_forms import PurchaseOrderForm
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fpdf import FPDF


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
def create_purchase_order():
    if request.method == 'POST':
        purchase_order_values = json.loads(request.form.get('values'))
        purchase_order_main_object = purchase_order_values.get('purchase_orderData')
        purchase_order_items = purchase_order_values.get('itemData')
        object = PurchaseOrder(purchase_order_state="Pending",
                               supplier_id=purchase_order_main_object.get('supplier_id'),
                               purchase_total=purchase_order_main_object.get('purchase_total'),
                               purchase_order_created_date=purchase_order_main_object.get('purchase_order_created_date'),
                               purchase_order_expected_date=purchase_order_main_object.get('purchase_order_expected_date'))
        db.session.add(object)
        db.session.flush()
        object.purchase_order_name = "PO" + str(('{0:05d}'.format(object.id)))
        db.session.commit()
        for item in purchase_order_items:
            item_obj = PurchaseOrderLine(quantity=item.get('quantity'), subtotal=item.get('subtotal'), unit_price=item.get('unit_price'), item_id=item.get('item_product_id'), purchase_order_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return jsonify(id=object.id)
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
            'purchase_order_created_date': purchase_order_main_object.get('purchase_order_created_date'),
            'purchase_order_expected_date': purchase_order_main_object.get('purchase_order_expected_date'),
            'purchase_total': purchase_order_main_object.get('purchase_total'),
        }
        id = purchase_order_main_object.get('id')
        PurchaseOrder.query.filter(PurchaseOrder.id==id).update(vals)
        db.session.commit()
        PurchaseOrderLine.query.filter(PurchaseOrderLine.purchase_order_id==id).delete()
        db.session.commit()
        for item in purchase_order_items:
            item_obj = PurchaseOrderLine(quantity=item.get('quantity'), subtotal=item.get('subtotal'), unit_price=item.get('unit_price'), item_id=item.get('item_product_id'), purchase_order_id=id)
            db.session.add(item_obj)
            db.session.commit()
        return jsonify(id=id)
    flash('Something went wrong.')
    return redirect(url_for('purchase_order_actions_controllers.edit_purchase_order_view'))


@purchase_order_actions_controllers.route('/view_confirmed_purchase_order', methods=["GET", "POST"])
@login_required
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
        return jsonify(id=po_id)
    return redirect(url_for('purchase_order_actions_controllers.edit_purchase_order_view'))


@purchase_order_actions_controllers.route('/create_grn', methods=["GET", "POST"])
@login_required
def create_grn():
    if request.method == 'POST':
        purchase_order_values = json.loads(request.form.get('values'))
        main_values = purchase_order_values.get('purchase_orderData')
        line_values = purchase_order_values.get('itemData')
        object = Grn(supplier_id=main_values.get('supplier_id'), grn_state="Receiving",
                     grn_created_date=datetime.now(),
                     po_id=main_values.get('id'),
                     grn_expected_date=main_values.get('purchase_order_expected_date'))
        db.session.add(object)
        db.session.flush()
        object.grn_name = "IN/" + str(('{0:05d}'.format(object.id)))
        db.session.commit()
        vals = {
            'purchase_order_state': "GRN Created",
        }
        PurchaseOrder.query.filter(PurchaseOrder.id == main_values.get('id')).update(vals)
        db.session.commit()
        for item in line_values:
            item_obj = GrnLine(item_id=item.get('item_product_id'), demand_quantity=item.get('quantity'),
                               received_quantity=0, remaining_quantity=item.get('quantity'),
                               grn_id=object.id)
            db.session.add(item_obj)
            db.session.commit()
        return jsonify(id=object.id)
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
        PurchaseOrderLine.query.filter(PurchaseOrderLine.purchase_order_id == id).delete()
        db.session.commit()
        PurchaseOrder.query.filter(PurchaseOrder.id == id).delete()
        db.session.commit()
        return redirect(url_for('purchase_order_actions_controllers.view_purchase_order'))


@purchase_order_actions_controllers.route('/download_pdf', methods=["GET", "POST"])
@login_required
def download_pdf():
    id = int(request.values.get('id'))
    po = PurchaseOrder.query.filter_by(id=id).first()
    # items_day_1 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day1').order_by('sequence').all()
    # items_day_2 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day2').order_by('sequence').all()
    # items_day_3 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day3').order_by('sequence').all()
    # items_day_4 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day4').order_by('sequence').all()
    # items_day_5 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day5').order_by('sequence').all()
    # items_day_6 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day6').order_by('sequence').all()
    # items_day_7 = ScheduleWorksheet.query.filter_by(schedule_id=id, day='day7').order_by('sequence').all()
    pdf = FPDF(format='letter', unit='in')
    # Add new page. Without this you cannot create the document.
    pdf.add_page()
    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    first_line = [["# - " + str(po.purchase_order_name), "Supplier - " + str(po.supplier.supplier_name)]]
    second_line = [["Created Date - " + str(po.purchase_order_created_date), "Expected Date - " + str(po.purchase_order_created_date)]]
    col_width = epw / 2
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(epw, 0.0, 'Purchase Order', align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.5)

    th = pdf.font_size * 2

    for row in first_line:
        for column in row:
            pdf.set_font('Times', 'B', 12.0)
            pdf.cell(col_width, th, str(column), border=1, align='C')
        pdf.ln(th)

    for row in second_line:
        for column in row:
            pdf.set_font('Times', 'B', 12.0)
            pdf.cell(col_width, th, str(column), border=1, align='C')
        pdf.ln(th)

    pdf.ln(0.5)

    col_width = epw / 4
    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    heading = [['Item', 'Quantity', 'Unit Price', 'Total Price']]
    data = []
    for line in po.purchase_order_line:
        data.append([line.item.item_name, line.quantity, line.unit_price, line.subtotal])
    # for line in items_day_2:
    #     data_2.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])
    # for line in items_day_3:
    #     data_3.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])
    # for line in items_day_4:
    #     data_4.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])
    # for line in items_day_5:
    #     data_5.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])
    # for line in items_day_6:
    #     data_6.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])
    # for line in items_day_7:
    #     data_7.append([line.sequence, line.day, line.workout.name, line.equipment.name, line.note, line.number_of_sets, line.number_of_reps])

    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(epw, 0.0, 'Items', align='C')
    pdf.set_font('Times', '', 10.0)
    pdf.ln(0.1)

    # Text height is the same as current font size
    th = pdf.font_size * 2

    for row in heading:
        for column in row:
            pdf.set_font('Times', 'B', 12.0)
            pdf.cell(col_width, th, str(column), border=1, align='C')
        pdf.ln(th)
    #
    for row in data:
        for column in row:
            pdf.set_font('Times', '', 10.0)
            pdf.cell(col_width, th, str(column), border=1)
        pdf.ln(th)
    #
    # for row in data_2:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)
    #
    # for row in data_3:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)
    #
    # for row in data_4:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)
    #
    # for row in data_5:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)
    #
    # for row in data_6:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)
    #
    # for row in data_7:
    #     for column in row:
    #         pdf.set_font('Times', '', 10.0)
    #         pdf.cell(col_width, th, str(column), border=1)
    #     pdf.ln(th)

    pdf.output('schedule.pdf', 'F')
    return send_from_directory(directory='./', filename='schedule.pdf')