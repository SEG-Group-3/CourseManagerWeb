from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email


class EditUserForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    role = SelectField("User Role", [DataRequired()], choices=[
        'Student', 'Instructor', 'Admin'])
    submit = SubmitField('Apply changes')
