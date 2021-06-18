from flask_login import login_manager
from app.models import User
from flask.globals import session
import flask_login
from app.auth.forms import LoginForm
from flask import Blueprint
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, request, url_for, flash
from ..database import users_db
from .. import login_manager
auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user_auth(userName):
    data = users_db.get_user(userName)
    return User(data) if data is not None else data


def is_valid_cred_auth(user: User):
    return users_db.is_valid_cred(user.data['userName'], user.data['password'])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Logging in")
    if form.validate_on_submit():
        user = load_user_auth(form.userName.data)
        print(user)
        if user is not None and is_valid_cred_auth(user):
            login_user(user, remember=True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.jinja', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@auth_bp.route("/whoami")
@login_required
def whoami():

    return "Your name is: " + flask_login.current_user.data['userName']
