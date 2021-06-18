from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    # password = PasswordField('Password',
    #                          validators=[DataRequired()])
    # userType = SelectField('User type', [DataRequired()], choices=[
    #                        "Student", "Instructor"])
    submit = SubmitField('Submit')
