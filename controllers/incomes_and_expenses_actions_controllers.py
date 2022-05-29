# importing libraries and files
import io

from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, send_from_directory, Response
from models.incomes_and_expenses import IncomesAndExpenses
from models.purchase_order import PurchaseOrder
from models.suppliers import Supplier
from models.users import User
from flask_login import login_required, current_user
from app import db
from fpdf import FPDF
from sqlalchemy import or_
# from forms.incomes_and_expenses_forms import CreateIncomesAndExpensesForm, CreateIncomesAndExpensesReportForm
import json
import xlwt
from datetime import datetime

incomes_and_expenses_actions_controller = Blueprint('incomes_and_expenses_actions_controller', __name__)

# view all incomes_and_expenses list
@incomes_and_expenses_actions_controller.route('/view_incomes_and_expenses', methods=["GET", "POST"])
@login_required
def view_incomes_and_expenses():
    incomes_and_expenses = IncomesAndExpenses.query.all()
    return render_template('incomes_and_expenses/incomes_and_expenses.html', incomes_and_expenses=incomes_and_expenses)


# load member create view
@incomes_and_expenses_actions_controller.route('/create_incomes_and_expenses_view', methods=["GET", "POST"])
@login_required
def create_incomes_and_expenses_view():
    return render_template('incomes_and_expenses/incomes_and_expenses_create.html', form=CreateIncomesAndExpensesForm(), type='create')


# create member when form is submitted
@incomes_and_expenses_actions_controller.route('/create_incomes_and_expenses', methods=["GET", "POST"])
@login_required
def create_incomes_and_expenses():
    create_incomes_and_expenses_from = CreateIncomesAndExpensesForm(request.form)
    if request.method == 'POST':
    #if create_incomes_and_expenses_from.validate():
        date = request.form['date']
        type = request.form['type']
        category = request.form['category']
        amount = request.form['amount']

        incomes_and_expenses = IncomesAndExpenses(date=date, type=type, category=category, amount=amount)
        db.session.add(incomes_and_expenses)
        db.session.flush()
        db.session.commit()
        flash('Successfully added!')
    return redirect(url_for('incomes_and_expenses_actions_controller.view_incomes_and_expenses'))


# load created member with form view
@incomes_and_expenses_actions_controller.route('/view_incomes_and_expenses_view', methods=["GET", "POST"])
@login_required
def view_incomes_and_expenses_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_incomes_and_expenses(id)
    return redirect(url_for('incomes_and_expenses_actions_controller.view_incomes_and_expenses'))


# normal function
def redirect_incomes_and_expenses(id):
    incomes_and_expenses = IncomesAndExpenses.query.filter_by(id=id).first()
    return render_template('incomes_and_expenses/incomes_and_expenses_create.html', form=CreateIncomesAndExpensesForm(), type='view', incomes_and_expenses=incomes_and_expenses)

# load member edit view
@incomes_and_expenses_actions_controller.route('/edit_incomes_and_expenses_view', methods=["GET", "POST"])
@login_required
def edit_incomes_and_expenses_view():
    id = int(request.values.get('id'))
    if id:
        incomes_and_expenses = IncomesAndExpenses.query.filter_by(id=id).first()
        return render_template('incomes_and_expenses/incomes_and_expenses_create.html', form=CreateIncomesAndExpensesForm(), type='edit', incomes_and_expenses=incomes_and_expenses)
    return redirect(url_for('incomes_and_expenses_actions_controller.view_incomes_and_expenses'))


# edit member when form is submitted
@incomes_and_expenses_actions_controller.route('/edit_incomes_and_expenses', methods=["GET", "POST"])
@login_required
def edit_incomes_and_expenses():
    if request.method == 'POST':
        vals = {
            'date': request.form['date'],
            'type': request.form['type'],
            'category': request.form['category'],
            'amount': request.form['amount'],
        }
        id = request.form['id']
        # existing_incomes_and_expenses = IncomesAndExpenses.query.filter(or_(IncomesAndExpenses.type==request.form['type'])).all()
        # if existing_incomes_and_expenses:
        IncomesAndExpenses.query.filter(IncomesAndExpenses.id==id).update(vals)
        db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect_incomes_and_expenses(id)
    flash('A member already exists with the Email address')
    return redirect(url_for('incomes_and_expenses_actions_controller.edit_incomes_and_expenses_view'))

@incomes_and_expenses_actions_controller.route('/delete_incomes_and_expenses', methods=["GET", "POST"])
@login_required
def delete_incomes_and_expenses():

    id = int(request.values.get('id'))
    if id:
        IncomesAndExpenses.query.filter(IncomesAndExpenses.id==id).delete()
        db.session.commit()
        return redirect(url_for('incomes_and_expenses_actions_controller.view_incomes_and_expenses', _anchor="content", ))


@incomes_and_expenses_actions_controller.route('/download_report_view', methods=["GET", "POST"])
@login_required
def download_report_view():
    create_incomes_and_expenses_from = CreateIncomesAndExpensesReportForm(request.form)
    if request.method == 'POST':
        # if create_incomes_and_expenses_from.validate():
        begin_date = request.form['begin_date']
        end_date = request.form['end_date']
    return redirect(url_for('incomes_and_expenses_actions_controller.download_report_view'))

@incomes_and_expenses_actions_controller.route('/download_report', methods=["GET", "POST"])
@login_required
def download_report():
    download_report_view_from = CreateIncomesAndExpensesReportForm(request.form)
    if request.method == 'POST':
        incomes_vs_dates = IncomesAndExpenses.query.filter(or_(IncomesAndExpenses.date==request.form['date'])).fetchall()
        income_vs_category = IncomesAndExpenses.query.filter(or_(IncomesAndExpenses.category==request.form['category'])).fetchall()
        incomes_vs_type = IncomesAndExpenses.query.filter(
            or_(IncomesAndExpenses.type == request.form['type'])).fetchall()
        incomes_vs_amount = IncomesAndExpenses.query.filter(
            or_(IncomesAndExpenses.amount == request.form['amount'])).fetchall()

        #output in bytes
        output = io.BytesIO()
        #create workbook object
        workbook = xlwt.Workbook()
        #add a sheet
        sh = workbook.add_sheet(('Incomes'))
        #add headers
        sh.write(0, 0, 'Id')
        sh.write(0, 1, 'type')
        sh.write(0, 2, 'category')
        sh.write(0, 3, 'amount')
        idx = 0
        for row in incomes_vs_dates:
            sh.write(idx + 1, 0, str(row[id]))
            sh.write(idx + 1, 1, str(row[incomes_vs_type]))
            sh.write(idx + 1, 2, str(row[income_vs_category]))
            sh.write(idx + 1, 3, str(row[incomes_vs_amount]))
            idx += 1
        workbook.save(output)
        output.seek(0)
        flash('Successfully downloaded!')
    return Response()









##############################################################################################
# @incomes_and_expenses_actions_controller.route('/download_po_purchase_order', methods=["GET", "POST"])
# @login_required
# def download_po_purchase_order():
#     id = int(request.values.get('id'))
#     purchase_order = PurchaseOrder.query.filter_by(id=id).first()
#     purchase_order_name = PurchaseOrder.query.filter_by(id=id).first()
#     purchase_order_created_date = PurchaseOrder.query.filter_by(id=id).first()
#     purchase_order_expected_date = PurchaseOrder.query.filter_by(id=id).first()
#     supplier_id = PurchaseOrder.query.filter_by(id=id).first()
#     item_id = PurchaseOrder.query.filter_by(id=id).first()
#     purchase_order_state = PurchaseOrder.query.filter_by(id=id).first()
#     supplier = PurchaseOrder.query.filter_by(id=id).first()
#     item = PurchaseOrder.query.filter_by(id=id).first()
#     purchase_order_line = PurchaseOrder.query.filter_by(id=id).first()
#     supplier_name = Supplier.query.filter_by(id=id).first()
#
#     items_day_1 = PurchaseOrder.query.filter_by(id=id, item_name_line='item_name_line').order_by('purchase_order_name').all()
#     items_day_2 = PurchaseOrder.query.filter_by(id=id, item_quantity_line='item_quantity_line').order_by('purchase_order_name').all()
#
#     pdf = FPDF(format='letter', unit='in')
#     # Add new page. Without this you cannot create the document.
#     pdf.add_page()
#     # Remember to always put one of these at least once.
#     pdf.set_font('Times', '', 10.0)
#     # Effective page width, or just epw
#     epw = pdf.w - 2 * pdf.l_margin
#     # Set column width to 1/4 of effective page width to distribute content
#     # evenly across table and page
#     first_line = [[purchase_order.purchase_order_name, purchase_order.supplier.supplier_name]]
#     second_line = [[purchase_order.purchase_order_created_date, purchase_order.purchase_order_expected_date]]
#     col_width = epw / 2
#     pdf.set_font('Times', 'B', 14.0)
#     pdf.cell(epw, 0.0, 'Purchase Order', align='C')
#     pdf.set_font('Times', '', 10.0)
#     pdf.ln(0.5)
#
#     th = pdf.font_size * 2
#
#     for row in first_line:
#         for column in row:
#             pdf.set_font('Times', 'B', 12.0)
#             pdf.cell(col_width, th, str(column), border=1, align='C')
#         pdf.ln(th)
#
#     for row in second_line:
#         for column in row:
#             pdf.set_font('Times', 'B', 12.0)
#             pdf.cell(col_width, th, str(column), border=1, align='C')
#         pdf.ln(th)
#
#     pdf.ln(0.5)
#
#     col_width = epw / 7
#     # Since we do not need to draw lines anymore, there is no need to separate
#     # headers from data matrix.
#     heading = [['Item', 'Quantity']]
#     data_1 = []
#     data_2 = []
#
#     for line in items_day_1:
#         data_1.append([line.item_name_line, line.item_quantity_line])
#     for line in items_day_2:
#         data_2.append([line.item_name_line, line.item_quantity_line])
#
#
#     # Document title centered, 'B'old, 14 pt
#     pdf.set_font('Times', 'B', 14.0)
#     pdf.cell(epw, 0.0, 'Purchase Order', align='C')
#     pdf.set_font('Times', '', 10.0)
#     pdf.ln(0.1)
#
#     # Text height is the same as current font size
#     th = pdf.font_size * 2
#
#     for row in heading:
#         for column in row:
#             pdf.set_font('Times', 'B', 12.0)
#             pdf.cell(col_width, th, str(column), border=1, align='C')
#         pdf.ln(th)
#
#     for row in data_1:
#         for column in row:
#             pdf.set_font('Times', '', 10.0)
#             pdf.cell(col_width, th, str(column), border=1)
#         pdf.ln(th)
#
#     for row in data_2:
#         for column in row:
#             pdf.set_font('Times', '', 10.0)
#             pdf.cell(col_width, th, str(column), border=1)
#         pdf.ln(th)
#
#     pdf.output('purchase_order.pdf', 'F')
#     return send_from_directory(directory='./', filename='purchase_order.pdf')
