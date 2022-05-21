from wtforms import Form, StringField, PasswordField, validators, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5
#from models.countries import Country
from wtforms.fields.html5 import DateField
from datetime import datetime


class ProductionOrderForm(Form):

    production_team_id = SelectField('Production Team', choices=[])
    item_product_id = SelectField('Items', choices=[])
    production_order_name = StringField('Name', validators=[Length(max=200)])
    production_order_created_date = DateField(format="%Y-%m-%d", default=datetime.today())
    production_order_expected_date = DateField(format="%Y-%m-%d")
    production_order_state = SelectField(choices=['Confirmed', 'Pending'])
    id = IntegerField('Id')