
from flask import Blueprint
from flask import g
from flask import json
from flask.globals import request
from flask.json import jsonify
from flask.templating import render_template
from flask_login.utils import login_required
import app.database.users_db as u_manage
from flask_restful import Api, abort
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
