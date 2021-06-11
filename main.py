# Enviroment Variables
import json
import base64
import os

# Flask Stuff
from flask import Flask
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


def error(message="No message Provided", code=501):
    return {"error": {
            "message": message,
            "code": code
            }
            }


def ok(message="No message Provided"):
    return {"success": {
            "message": message,
            "code": 200
            }
            }


@app.route('/register')
def register():
    name = request.args.get('name', default="", type=str)
    password = request.args.get('password', default="", type=str)
    usertype = request.args.get('type', default="Student", type=str)

    user_ref = db.collection("Users")
    if password == "":
        return error("Missing Password", 422)
    if name == "":
        return error("Missing Name", 422)

    user_ref.add({'name': name, 'password': password, 'type': usertype})

    return ok("Account created")


@app.route('/')
def main():
    return error("Page not implemented")


@app.route('/courses')
def get():
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


if __name__ == '__main__':
    app.run(debug=True)
