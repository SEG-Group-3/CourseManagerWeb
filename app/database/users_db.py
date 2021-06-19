from os import truncate
from app.models import User
from . import db
from .. import login_manager

USERS_REF = db.collection("Users")
CACHE = {}

# Updates cache


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "ADDED" or change.type.name == "MODIFIED":
            change_dict = change.document.to_dict()
            CACHE[change.document.id] = change_dict
        elif change.type.name == "REMOVED":
            del CACHE[change.document.id]


WATCH = USERS_REF.on_snapshot(on_snapshot)


def get_uid_from_username(username):
    for uid, values in CACHE.items():
        if values.get("userName") == username:
            return uid
    return None


def get_user(username) -> dict:
    uid = get_uid_from_username(username)
    if uid == None:
        return None
    return CACHE.get(uid)


def get_users() -> dict:
    return CACHE


def search_users(query):
    results = {}
    for key, values in CACHE.items():
        if query in values["userName"] or query in values["realName"]:
            results[key] = values
    return results


def add_user(user: dict) -> bool:
    if get_user(user['userName']) is not None:  # User already exists
        return False
    USERS_REF.add(User.validate(user))
    return True


def update_user(user: dict) -> bool:
    doc_id = get_uid_from_username(user["userName"])
    if doc_id is None:
        return False
    user = User.validate(user)
    # Remove none fields
    u_copy = {k: v for k, v in user.items() if v != None and v != ''}
    USERS_REF.document(doc_id).update(u_copy)
    return True


def remove_user(username):
    doc_uid = get_uid_from_username(username)
    if doc_uid is not None:
        USERS_REF.document(doc_uid).delete()


def is_valid_cred(username, password) -> bool:
    actual = get_user(username)
    if actual is None:
        return False
    return actual["password"] == password
