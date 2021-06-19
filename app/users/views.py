
from app.models import User
from flask.helpers import flash
from app.users.forms import EditUserForm
from flask import Blueprint
from flask import g
from flask import json
from flask.globals import request
from flask.json import jsonify
from flask.templating import render_template
from flask_login.utils import login_required
import app.database.users_db as u_manage
from flask_restful import abort
users_bp = Blueprint('users', __name__)


@users_bp.route("/")
@login_required
def users():
    u_data = u_manage.get_users()
    u_data = list(u_data.values())
    return render_template("users/users.jinja", user_data=u_data)


@users_bp.route("/get", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return jsonify(u_manage.get_users())
    if request.method == "POST":
        u_manage.add_user(request.form)
        return ("", 204)


@users_bp.route("/<username>", methods=["GET", "PUT", "DELETE"])
@login_required
def user_info(username):
    user_dict = u_manage.get_user(username)
    if user_dict is None:
        abort(404)
    if request.method == "PUT":
        user_dict.update(dict(request.form))
        u_manage.update_user(user_dict)
    if request.method == "DELETE":
        u_manage.remove_user(username)
        return ("", 204)
    return jsonify(user_dict)


@users_bp.route("/edit/<user>", methods=["GET", "POST"])
@login_required
def edit_user(user):
    form = EditUserForm()
    just_updated = False
    current_u = u_manage.get_user(user)
    if form.validate_on_submit():
        if current_u is not None:  # Check if course still exists
            if form.userName.data != user and u_manage.get_user(form.userName.data) is not None:
                # The name we are changing to already exists! Abort
                flash(f'The username "{form.userName.data}" is already taken!')
            else:
                u = User.validate({"userName": form.userName.data,
                                  "type": form.role.data, "password": form.password.data})
                # We won't be changin the course code... for now
                u_manage.update_user(u)
                flash('User edited!')
            just_updated = True
        else:
            flash('The current course has been modified or deleted')

    # Just get the initial values

    if just_updated:
        form.userName.data = form.userName.data
        form.password.data = form.password.data
        form.role.data = form.role.data
    else:
        form.userName.data = current_u['userName']
        form.password.data = current_u['password']
        form.role.data = current_u['type']

    return render_template("users/create.jinja", form=form)
