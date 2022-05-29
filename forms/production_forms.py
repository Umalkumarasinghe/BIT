from wtforms import Form, StringField, PasswordField, validators, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5
#from models.countries import Country
from wtforms.fields.html5 import DateField
from datetime import datetime


class ProductionForm(Form):

    team_id = SelectField('Team', choices=[])
    item_product_id = SelectField('Items', choices=[])
    production_name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    production_created_date = DateField('Production Date', format="%Y-%m-%d", default=datetime.today())
    production_expected_date = DateField(format="%Y-%m-%d")
    production_state = SelectField(choices=['Confirmed', 'Pending'])
    id = IntegerField('Id')