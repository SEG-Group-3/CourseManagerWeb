import base64
import json
import os

# Firebase
import firebase_admin as fb
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase credentials
if "AUTH" in os.environ:  # Load authentication from enviroment
    cred_string = base64.b64decode(os.environ["AUTH"]).decode("UTF-8")
else:  # Load authentication from local file
    cred_string = open("keys.json").read()

cred = credentials.Certificate(json.loads(cred_string))
fb.initialize_app(cred)
db = firestore.client()
