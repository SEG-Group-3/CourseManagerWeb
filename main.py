# Token managing and creation
from datetime import datetime, timedelta
import secrets



# Function Wrapping
import functools

# Enviroment Variables
import json
import base64
import os

# Flask Stuff
from flask import Flask, wrappers
from flask_restful import Api
from flask_cors import CORS

# Firebase
import firebase_admin as fb
from firebase_admin import credentials
from firebase_admin import firestore
from flask import request
from google.auth.credentials import CredentialsWithQuotaProject

# Initialize Firebase credentials
if("AUTH" in os.environ): # Load authentication from enviroment
    cred_string = base64.b64decode(os.environ["AUTH"]).decode('UTF-8')
else: # Load authentication from local file
    cred_string = open("keys.json").read()

cred = credentials.Certificate(json.loads(cred_string))
fb.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
api = Api(app)
CORS(app)


def status(status_type="ok", message="No message Provided", code=501):
    return {status_type: {
            "message": message,
            "code": code
            }
        }

def error(message="No message Provided", code=501):
    return status("error", message, code)

def ok(message="No message Provided"):
    return status("success", message, 200)

# Verifies that all parameters are passed before executing the function
def param_required(_func=None, *, params=[]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for param in params:
                arg_val = request.args.get(param, default=None, type=str)
                if arg_val == None:
                    return error(f"Missing parameter: {param}", 401)
            return func(*args, **kwargs)
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

# Requires an auth token and an access requirement
def token_required(_func=None, *, allowed_users=[], blocked_users=[]):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Verify if token is valid
            active_ref = db.collection("activeAccounts")

            token = request.args.get("token", default=None, type=str)
            if token == None:
                return error(f"Missing parameter: token", 401)

            user_uid = None
            ok = False
            for toks in active_ref.stream():
                toks_data = toks.to_dict()
                token_matches = toks_data['token'] == token
                if(token_matches):
                    expiration_date = datetime.fromisoformat(toks_data['expiration'])
                    present = datetime.now()
                    if(expiration_date > present): # Token Is still valid
                        user_uid = toks_data['userName']
                        ok =True
                    break

            if not ok:
                # Redirect to login?
                return error(f"Invalid Token", 440)

            # Verify if token is expired



            # Verify access requirement
            user_ref = db.collection("Users").document(user_uid).get()
            user_dict = user_ref.to_dict()

            for u_type in blocked_users:
                if user_dict['type'] == u_type:
                    return error(f"{user_dict['type']} is not allowed access", 401)

            for u_type in allowed_users:
                if user_dict['type'] == u_type:
                    return func(*args, **kwargs)

            return func(*args, **kwargs)
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

@app.route('/login')
@param_required(params=['name', 'password'])
def login():
    # Validate credentials
    name = request.args.get('name', type=str)
    password = request.args.get('password', type=str)

    users_ref = db.collection("Users")
    working_user = None
    for user in users_ref.stream():
        userdata = user.to_dict()
        if(userdata['userName'] == name):
            if(userdata['password'] == password):
                working_user = user
            break

    if working_user == None:
        return error("Invalid username or password")

    # If previous token exist, delete it and create new
    active_ref = db.collection("activeAccounts")

    for toks in active_ref.stream():
        toks_data = toks.to_dict()
        if(toks_data['userName'] == working_user.id):
            # Token already exists, delete it!
            active_ref.document(toks.id).delete()
            break

    # Create a new token for the user
    expiration = datetime.now() + timedelta(minutes=10)
    expiration_str = expiration.isoformat()
    token = secrets.token_urlsafe(32)
    token_response = {'userName': working_user.id, 'token': token, 'expiration': expiration_str}
    active_ref.add(token_response)
    return ok(token_response)

@app.route('/register')
@param_required(params=['name', 'password'])
def register():
    name = request.args.get('name', type=str)
    password = request.args.get('password', type=str)
    usertype = request.args.get('type', default="Student", type=str)

    user_ref = db.collection("Users")
    user_ref.add({'userName': name, 'password': password, 'type': usertype})

    return ok("Account created")

@app.route('/')
def home():
    return error("Page not implemented, go read the README.md!")

@app.route('/sneed')
def sneed():
    return {"and" : "feed"}


@app.route('/courses')
def get_courses():
    courses = {}

    name_filter = request.args.get('name', default="", type=str)
    code_filter = request.args.get('code', default="", type=str)

    courses_ref = db.collection("Courses")
    for doc in courses_ref.stream():
        course_dict = doc.to_dict()
        if name_filter.lower() not in course_dict["name"].lower():
            continue
        if code_filter.lower() not in course_dict["code"].lower():
            continue
        courses[doc.id] = course_dict

    return courses

@app.route('/users')
@token_required(blocked_users=['Student'])
def get_users():
    users = {}
    name_filter = request.args.get('name', default="", type=str)
    users_ref = db.collection("Users")
    for doc in users_ref.stream():
        user_dict = doc.to_dict()
        if name_filter.lower() not in user_dict["userName"].lower():
            continue
        users[doc.id] = user_dict
    return users


@app.route('/courses/add')
@param_required(params=['code', 'name', 'token'])
@token_required(allowed_users=['Admin'])
def add_course():
    name = request.args.get('name', type=str)
    code = request.args.get('code', type=str)

    courses_ref = db.collection("Courses")

    course_data_object = {'code': code, 'name': name}
    courses_ref.add(course_data_object)
    return ok("Course Added")

if __name__ == '__main__':
    app.run(debug=True)
