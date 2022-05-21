# importing libraries and files
from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5


# initiating the class
class CreateSupplierForm(Form):

    # form fields
    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=200)])
    supplier_email = StringField('E-mail Address', validators=[DataRequired(), Length(max=255)])
    supplier_contact_no = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    supplier_address = StringField('Address', validators=[DataRequired(), Length(max=50)])
    id = IntegerField('Id')