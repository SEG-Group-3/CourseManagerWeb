
from flask import request
from ..plugins import sio
from ..database import users_db as u_manage


@sio.event
def users_search(message):
    print("User " + str(request.sid) + " is searching... " + message['data'])

    users_found = list(u_manage.search_users(message['data']).values())

    if len(users_found) > 0:
        sio.emit('users_result', {'data': users_found}, to=request.sid)
