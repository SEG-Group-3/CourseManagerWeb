from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, close_room, rooms, disconnect
from . import create_app

app = create_app()
socketio = SocketIO(app, async_mode="gevent")
socketio.init_app
socketio.run(app)
thread = None
thread_lock = Lock()
