from app.models import Course
from . import db
from difflib import get_close_matches
COURSES_REF = db.collection("Courses")
CACHE = {}

# Updates cache

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "ADDED" or change.type.name == "MODIFIED":
            change_dict = change.document.to_dict()
            CACHE[change.document.id] = change_dict
        elif change.type.name == "REMOVED":
            del CACHE[change.document.id]


WATCH = COURSES_REF.on_snapshot(on_snapshot)


def get_course_from_uid(uid):
    return CACHE.get(uid)


def get_uid_from_code(code):
    for uid, values in CACHE.items():
        if values.get("code") == code:
            return uid
    return None


def get_course(code):
    for values in CACHE.keys():
        if CACHE[values]["code"] == code:
            return CACHE[values]


def search_courses(query):
    results = {}
    query = query.lower()
    close_names = get_close_matches(
        query, (n['name'].lower() for n in CACHE.values()))
    close_codes = get_close_matches(
        query, (n['code'].lower() for n in CACHE.values()))

    for key, values in CACHE.items():
        if values["code"].lower() in close_codes or values["name"].lower() in close_names:
            results[key] = values
        elif query in values["code"].lower() or query in values["name"].lower():
            results[key] = values
    return results


def get_courses() -> dict:
    return CACHE


def add_course(course: dict):
    # We should check for repeated userNames
    COURSES_REF.add(Course.validate(course))


def update_course(course: dict) -> bool:
    doc_id = get_uid_from_code(course["code"])
    if doc_id is None:
        return False
    course = Course.validate(course)
    c_copy = {k: v for k, v in course.items() if v != None and v != ''}
    COURSES_REF.document(doc_id).update(c_copy)
    return True


def remove_course(course_code):
    doc_uid = get_uid_from_code(course_code)
    if doc_uid is not None:
        COURSES_REF.document(doc_uid).delete()
