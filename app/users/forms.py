from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    role = SelectField("User Role", [DataRequired()], choices=[
        'Student', 'Instructor', 'Admin'])
    submit = SubmitField('Apply changes')
