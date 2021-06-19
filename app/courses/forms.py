from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditCourseForm(FlaskForm):
    courseName = StringField('Course Name', validators=[DataRequired()])
    code = StringField('Course Code', validators=[DataRequired()])
    submit = SubmitField('Apply changes')
