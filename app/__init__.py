from flask_cors.extension import CORS
from flask_login.login_manager import LoginManager
from flask_bootstrap import Bootstrap

"""
Chat Server
===========
This simple application uses WebSockets to run a primitive chat server.
"""

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(args=None):
    from flask import Flask, render_template,  session, redirect, url_for, flash
    from app.users import users_bp
    from app.courses import courses_bp
    from .auth import auth_bp

    app = Flask(__name__)
    app.secret_key = "secret"
    app.url_map.strict_slashes = False

    bootstrap.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.jinja')

    # socketio.init_app(app)
    return app
