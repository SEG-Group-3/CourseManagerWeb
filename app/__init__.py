from flask_cors.extension import CORS
from flask_login.login_manager import LoginManager
from flask_bootstrap import Bootstrap
from app.forms.user_form import NameForm

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
        print(session)
        form = NameForm()
        if form.validate_on_submit():
            old_name = session.get('name')
            print("Old name: " + str(old_name))
            print("New name: " + str(form.name.data))
            if old_name is not None and old_name != form.name.data:
                print("Changing name!")
                flash(
                    f'Looks like you have changed your name to {form.name.data}!')
            session['name'] = form.name.data
            return redirect(url_for('index'))
        return render_template('index.jinja', form=form, name=session.get('name'))

    # socketio.init_app(app)
    return app
