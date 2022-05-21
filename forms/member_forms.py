# importing libraries and files
from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5


# initiating the class
class CreateMemberForm(Form):

    # form fields
    full_name = StringField('Name In Full', validators=[DataRequired(), Length(max=200)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    calling_name = StringField('Calling Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    nic_no = StringField('NIC Number', validators=[DataRequired(), Length(max=12)])
    date_of_birth = DateField('Date of Birth', validators=[])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField(choices=[('male', 'Male'), ('female', 'Female')])
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    emergency_contact = StringField('Emergency Contact Person Name', validators=[DataRequired(), Length(max=120)])
    emergency_contact_no = StringField('Emergency Contact Phone Number', validators=[DataRequired(), Length(max=20)])
    emergency_contact_relationship = StringField('Emergency Contact Relationship', validators=[DataRequired(), Length(max=120)])
    id = IntegerField('Id')