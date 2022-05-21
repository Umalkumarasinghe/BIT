from wtforms import Form, StringField, PasswordField, validators, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5
from wtforms.fields.html5 import DateField
from datetime import datetime


class PurchaseOrderForm(Form):
    supplier_id = SelectField('Supplier', choices=[])
    item_product_id = SelectField('Items', choices=[])
    purchase_order_name = StringField('Name', validators=[Length(max=200)])
    purchase_order_created_date = DateField(format="%Y-%m-%d", default=datetime.today())
    purchase_order_expected_date = DateField(format="%Y-%m-%d")
    purchase_total = IntegerField('Total', validators=[DataRequired()], default=55)
    id = IntegerField('Id')