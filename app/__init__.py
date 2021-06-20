

def create_app(args=None):
    from flask_cors.extension import CORS
    from flask import Flask, render_template
    from .users import users_bp
    from .courses import courses_bp
    from .auth import auth_bp
    from .plugins import sio, bootstrap, login_manager, api

    app = Flask(__name__)
    app.secret_key = "secret"
    app.url_map.strict_slashes = False

    # Init plugins
    sio.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)
    CORS(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.jinja')

    return app


def run_app():
    pass
