from flask import render_template, redirect, Blueprint, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from auth_app.forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user


login_page_views = Blueprint('login_page_views', __name__, template_folder='templates')


@login_page_views.route('/login')
def login():
    form = LoginForm()
    return render_template('auth_app/login.html', form=form)


@login_page_views.route('/login', methods=['POST'])
def login_post():
    from auth_app.models import User
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    remember_me = form.remember_me.data
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Your email or password is invalid, check your credentials and try again.')
        return redirect(url_for('login_page_views.login'))
    login_user(user, remember=remember_me)
    return redirect(url_for('login_page_views.profile'))


@login_page_views.route('/signup')
def signup():
    form = LoginForm()
    return render_template('auth_app/signup.html', form=form)


@login_page_views.route('/signup', methods=['POST'])
def signup_post():
    from app import db
    from auth_app.models import User
    form = LoginForm()
    email = form.email.data
    username = form.username.data
    password = form.password.data
    user_mail = User.query.filter_by(email=email).first()
    user_name = User.query.filter_by(username=username).first()
    if user_mail or user_name:
        flash('This username/email is already exists')
        return redirect(url_for('login_page_views.signup'))
    create_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(create_user)
    db.session.commit()
    return redirect(url_for('login_page_views.login'))


@login_page_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You successfully logged out!')
    return redirect(url_for('index'))


@login_page_views.route('/profile')
@login_required
def profile():
    return render_template('auth_app/profile.html', name=current_user.username)