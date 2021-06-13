# Flask Stuff
from flask import Flask, abort, jsonify
from flask.globals import request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

# Database
import course_manager as c_manage
import user_manager as u_manage

# Initialize Flask Application
app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)
auth = HTTPBasicAuth()
CORS(app)


@auth.verify_password
def verify_password(name, password=None):

    if u_manage.is_valid_credential(name, password):
        return name
    return None


@app.route("/whoami")
def whoami():
    return auth.username() if auth.username() is not None else "Not logged in"


@app.route("/users", methods=["GET", "POST"])
@app.route("/users")
def users():
    if request.method == "GET":
        return jsonify(u_manage.get_users())
    if request.method == "POST":
        u_manage.add_user(request.form)
        return ("", 204)


@app.route("/users/<username>", methods=["GET", "PUT", "DELETE"])
def user(username):
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


@app.route("/courses", methods=["GET", "POST"])
@app.route("/courses")
def courses():
    if request.method == "GET":
        return jsonify(c_manage.get_courses())
    if request.method == "POST":
        c_manage.add_course(request.form)
    return ("", 204)


@app.route("/courses/<code>", methods=["GET", "PUT", "DELETE"])
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


@app.route("/")
def home():
    if auth is not None:
        return f"Welcome '{auth.username()}' !"
    return "Welcome!"


if __name__ == "__main__":
    app.run(debug=True)
