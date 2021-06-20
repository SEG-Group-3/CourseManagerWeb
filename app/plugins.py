from flask_login.login_manager import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_restful import Api

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
sio = SocketIO(logger=True, async_mode="gevent")
api = Api()
