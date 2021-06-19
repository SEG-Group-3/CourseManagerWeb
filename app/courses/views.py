
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from app.courses.forms import EditCourseForm
from flask import Blueprint
from flask import g
from flask.globals import request
from flask.json import jsonify
from flask.templating import render_template
from flask_login.utils import login_required
import app.database.courses_db as c_manage
from flask_restful import Api, abort

courses_bp = Blueprint('courses', __name__)


@courses_bp.route("/", methods=["GET", "POST"])
@login_required
def courses():
    c_data = c_manage.get_courses()
    c_data = list(c_data.values())
    return render_template("courses/courses.jinja", course_data=c_data)


@courses_bp.route("/edit/<code>", methods=["GET", "POST"])
@login_required
def edit_course(code):
    form = EditCourseForm()
    just_updated = False
    if form.validate_on_submit():
        current_c = c_manage.get_course(code)
        if current_c is not None:  # Check if course still exists
            if form.code.data != code and c_manage.get_course(form.code.data) is not None:
                # The name we are changing to already exists! Abort
                flash(f'The course code "{form.code.data}" is already taken!')
            else:
                c_manage.update_course(
                    {"code": form.code.data, "name": form.courseName.data})  # We won't be changin the course code... for now
                flash('Course edited!')
            just_updated = True
        else:
            flash('The current course has been modified or deleted')

    # Just get the initial values
    c_data = c_manage.get_course(code)
    if just_updated:
        form.courseName.data = form.courseName.data
        form.code.data = code
    else:
        form.courseName.data = c_data['name']
        form.code.data = c_data['code']
    return render_template("courses/create.jinja", form=form)


@courses_bp.route("/<code>", methods=["GET", "PUT", "DELETE"])
@login_required
def course(code):
    course_dict = c_manage.get_course(code)
    if course_dict is None:
        abort(404)
    if request.method == "PUT":
        course_dict.update(dict(request.form))
        c_manage.update_course(course_dict)
    if request.method == "DELETE":
        c_manage.remove_course(code)
        return ("", 204)
    return jsonify(course_dict)
