
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


@courses_bp.route("/<code>", methods=["GET", "PUT", "DELETE"])
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
