
from flask import request, jsonify
from ..plugins import sio
import flask
from ..database import courses_db as c_manage


@sio.event
def courses_search(message):
    print("User " + str(request.sid) + " is searching... " + message['data'])

    courses_found = list(c_manage.search_courses(message['data']).values())
    # payload = jsonify(courses_found)
    if len(courses_found) > 0:
        sio.emit('courses_result', {'data': courses_found}, to=request.sid)
