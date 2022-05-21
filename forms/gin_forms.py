from wtforms import Form, StringField, PasswordField, validators, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5
#from models.countries import Country
from wtforms.fields.html5 import DateField
from datetime import datetime


class GinForm(Form):

    production_team_id = SelectField('production_team', choices=[])
    item_product_id = SelectField('Items', choices=[])
    gin_name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    gin_created_date = DateField(format="%Y-%m-%d", default=datetime.today())
    gin_expected_date = DateField(format="%Y-%m-%d")
    gin_state = SelectField(choices=['Confirmed', 'Pending'])
    id = IntegerField('Id')