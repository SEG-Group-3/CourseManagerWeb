import socketio


# standard Python
sio = socketio.Client('http://localhost:5000')


@sio.event
def my_event(sid, data):
    # handle the message
    return "OK", 123


@sio.on('connect')
def on_connect():
    print("I'm connected!")


# sio.disconnect()
