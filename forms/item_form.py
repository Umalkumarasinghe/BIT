# importing libraries and files
from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5


# initiating the class
class CreateItemForm(Form):

    # form fields
    item_name = StringField('Items Name', validators=[DataRequired(), Length(max=200)])
    item_code = StringField('Items Code', validators=[DataRequired(), Length(max=255)])
    item_quantity = IntegerField('Items Quantity', validators=[DataRequired()])
    item_unit_price = IntegerField('Items Unit Price', validators=[DataRequired()])
    id = IntegerField('Id')