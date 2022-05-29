from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from models.users import User
from models.purchase_order import PurchaseOrder
from models.incomes_and_expenses import IncomesAndExpenses
from flask_login import login_user, current_user, login_required, logout_user
import app
from app import db
from sqlalchemy import or_
from forms.user_forms import CreateUserForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
from datetime import datetime
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

user_actions_controller = Blueprint('user_actions_controller', __name__)


@user_actions_controller.route('/')
def default():
    if current_user.is_authenticated:
        income_vs_expense = db.session.query(db.func.sum(IncomesAndExpenses.amount), IncomesAndExpenses.type).group_by(
            IncomesAndExpenses.type).order_by(IncomesAndExpenses.type).all()

        category_comparison = db.session.query(db.func.sum(IncomesAndExpenses.amount),
                                               IncomesAndExpenses.category).group_by(
            IncomesAndExpenses.category).order_by(IncomesAndExpenses.category).all()

        dates = db.session.query(db.func.sum(IncomesAndExpenses.amount), IncomesAndExpenses.date).group_by(
            IncomesAndExpenses.date).order_by(IncomesAndExpenses.date).all()

        purchase_order_vs_status = db.session.query(db.func.sum(PurchaseOrder.id),
                                                    PurchaseOrder.purchase_order_state).group_by(
            PurchaseOrder.purchase_order_state).order_by(PurchaseOrder.purchase_order_state).all()

        income_category = []
        for amounts, _ in category_comparison:
            income_category.append(amounts)

        income_expense = []
        for total_amount, _ in income_vs_expense:
            income_expense.append(total_amount)

        over_time_expenditure = []
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_expenditure.append(amount)

        purchase_order_status = []
        for purchase_orders, _ in purchase_order_vs_status:
            purchase_order_status.append(purchase_orders)

        return render_template('base/index.html',
                               income_vs_expense=json.dumps(income_expense),
                               income_category=json.dumps(income_category),
                               purchase_order_status=json.dumps(purchase_order_status),
                               over_time_expenditure=json.dumps(over_time_expenditure),
                               dates_label=json.dumps(dates_label)
                               )
        #confirmed_orders_vs_pending_orders = db.session.PurchaseOrder.purchase_order_state.group_by().all()
        #confirmed_orders_vs_pending_orders = []
        #for

        #return render_template('base/index.html')
    return render_template('user/login.html')




@user_actions_controller.route('/login', methods=["GET", "POST"])
def login():
    if request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            login_user(user)
            User.query.filter(User.id==user.id).update({'active': True, 'last_login': datetime.now()})
            db.session.commit()

            income_vs_expense = db.session.query(db.func.sum(IncomesAndExpenses.amount),
                                                 IncomesAndExpenses.type).group_by(
                IncomesAndExpenses.type).order_by(IncomesAndExpenses.type).all()

            category_comparison = db.session.query(db.func.sum(IncomesAndExpenses.amount),
                                                   IncomesAndExpenses.category).group_by(
                IncomesAndExpenses.category).order_by(IncomesAndExpenses.category).all()

            dates = db.session.query(db.func.sum(IncomesAndExpenses.amount), IncomesAndExpenses.date).group_by(
                IncomesAndExpenses.date).order_by(IncomesAndExpenses.date).all()

            purchase_order_vs_status = db.session.query(db.func.sum(PurchaseOrder.id), PurchaseOrder.purchase_order_state).group_by(
                PurchaseOrder.purchase_order_state).order_by(PurchaseOrder.purchase_order_state).all()

            income_category = []
            for amounts, _ in category_comparison:
                income_category.append(amounts)

            income_expense = []
            for total_amount, _ in income_vs_expense:
                income_expense.append(total_amount)

            over_time_expenditure = []
            dates_label = []
            for amount, date in dates:
                dates_label.append(date.strftime("%m-%d-%y"))
                over_time_expenditure.append(amount)

            purchase_order_status = []
            for purchase_orders, _ in purchase_order_vs_status:
                purchase_order_status.append(purchase_orders)

            return render_template('base/index.html',
                                   income_vs_expense=json.dumps(income_expense),
                                   income_category=json.dumps(income_category),
                                   purchase_order_status=json.dumps(purchase_order_status),
                                   over_time_expenditure=json.dumps(over_time_expenditure),
                                   dates_label=json.dumps(dates_label)
                                   )
            return render_template('base/index.html')
        else:
            flash("Invalid Email/Password")
            return redirect(url_for('user_actions_controller.default'))
    else:
        return redirect(url_for('user_actions_controller.default'))


@user_actions_controller.route('/view_users', methods=["GET", "POST"])
@login_required
def view_users():
    users = User.query.all()
    return render_template('user/users.html', users=users)


@user_actions_controller.route('/create_users_view', methods=["GET", "POST"])
@login_required
def create_users_view():
    return render_template('user/users_create.html', form=CreateUserForm(), type='create')


@user_actions_controller.route('/create_user', methods=["GET", "POST"])
@login_required
def create_user():
    create_user_from = CreateUserForm(request.form)
    if request.method == 'POST':
        if create_user_from.validate():
            email = request.form['email']
            password = request.form['password']
            active = False
            full_name = request.form['full_name']
            calling_name = request.form['calling_name']
            nic = request.form['nic']
            contact_no = request.form['contact_no']
            address = request.form['address']
            existing_user = User.query.filter(or_(User.nic == nic, User.email == email)).first()
            if not existing_user:
                user = User(email=email, password=password, active=active, full_name=full_name, calling_name=calling_name, last_login=None, last_logout=None, nic=nic, contact_no=contact_no, address=address)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user_actions_controller.view_users'))
        flash('A user already exists with the NIC/Email address')
    return redirect(url_for('user_actions_controller.view_users'))


@user_actions_controller.route('/view_user_view', methods=["GET", "POST"])
@login_required
def view_user_view():
    id = int(request.values.get('id'))
    if id:
        return redirect_user(id)
    return redirect(url_for('user_actions_controller.view_users'))


def redirect_user(id):
    user = User.query.filter_by(id=id).first()
    return render_template('user/users_create.html', form=CreateUserForm(), type='view', user=user)


@user_actions_controller.route('/edit_user_view', methods=["GET", "POST"])
@login_required
def edit_user_view():
    id = int(request.values.get('id'))
    if id:
        user = User.query.filter_by(id=id).first()
        return render_template('user/users_create.html', form=CreateUserForm(), type='edit', user=user)
    return redirect(url_for('user_actions_controller.view_users'))


@user_actions_controller.route('/edit_user', methods=["GET", "POST"])
@login_required
def edit_user():
    if request.method == 'POST':
        vals = {
            'full_name': request.form['full_name'],
            'address': request.form['address'],
            'calling_name': request.form['calling_name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'contact_no': request.form['contact_no'],
        }

        id = request.form['id']
        #current_user = User.query.filter(User.id==id).first()
        existing_user = User.query.filter(or_(User.email==request.form['email'])).all()
        if existing_user:
            User.query.filter(User.id == id).update(vals)
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect_user(id)
    flash('A user already exists with the NIC/Email address')
    return redirect(url_for('user_actions_controller.edit_user_view'))


@user_actions_controller.route('/delete_user', methods=["GET", "POST"])
@login_required
def delete_user():
    id = int(request.data)
    if id:
        User.query.filter(User.id==id).delete()
        db.session.commit()
        return redirect(url_for('user_actions_controller.view_users', _anchor="content", ))


@user_actions_controller.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    User.query.filter(User.id==current_user.id).update({'last_logout': datetime.now()})
    db.session.commit()
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('user_actions_controller.default'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='customer.umalonline7@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('user_actions_controller.reset_token', token=token, _external=True)}'''
    app.mail.send(msg)


@user_actions_controller.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return render_template('base/index.html')
    form = RequestResetForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has sent with instructions. to rest your password.', 'info')
        return redirect(url_for('user_actions_controller.login'))
    return render_template('user/reset_request.html', form=RequestResetForm())


@user_actions_controller.route('/reset_token/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return render_template('base/index.html')
    user = User.verify_reset_token(token=token)
    if not user:
        flash('The token is invalid or expired', 'warning')
        return redirect(url_for('user_actions_controller.reset_request'))
    form = ResetPasswordForm(request.form)
    if form.validate():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('user_actions_controller.login'))
    return render_template('user/reset_token.html', form=ResetPasswordForm())



