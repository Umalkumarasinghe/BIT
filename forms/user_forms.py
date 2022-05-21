from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5
from models.users import User


class CreateUserForm(Form):
    full_name = StringField('Name In Full', validators=[DataRequired(), Length(max=200)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    calling_name = StringField('Calling Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    nic_no = StringField('NIC Number', validators=[DataRequired(), Length(max=12)])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    access_group = SelectField('User Group', choices=[('Director', 'Director'), ('Manager', 'Manager'), ('DataEntryOparator', 'DataEntryOparator')])
    id = IntegerField('Id')


class RequestResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Hi")


class ResetPasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])