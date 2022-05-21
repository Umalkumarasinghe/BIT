# importing libraries and files
from wtforms import Form, StringField, PasswordField, validators, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import html5


# initiating the class
class CreateProductionTeamForm(Form):

    # form fields
    production_team_name = StringField('Production Team Name', validators=[DataRequired(), Length(max=200)])
    production_team_email = StringField('E-mail Address', validators=[DataRequired(), Length(max=255)])
    production_team_contact_no = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    production_team_address = StringField('Address', validators=[DataRequired(), Length(max=50)])
    id = IntegerField('Id')