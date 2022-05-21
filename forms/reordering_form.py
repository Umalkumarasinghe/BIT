# importing libraries and files
from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5


# initiating the class
class CreateItemForm(Form):

    # form fields
    item_name = StringField('Items Name', validators=[DataRequired(), Length(max=200)])
    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=255)])
    maximum_quantity = IntegerField('Maximum Quantity', validators=[DataRequired()])
    minimum_quantity = IntegerField('Minimum Quantity', validators=[DataRequired()])
    id = IntegerField('Id')