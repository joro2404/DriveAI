from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db, secret_key
from itsdangerous import URLSafeTimedSerializer, SignatureExpired



auth = Blueprint('auth', __name__)

serializer = URLSafeTimedSerializer(secret_key)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'danger')
        return redirect(url_for('main.index'))

    else:
        if request.method == 'GET':
            return render_template('login.html')

        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login credentials!', 'danger')
                return redirect(url_for('auth.login'))
                
            if not user.is_confirmed:
                flash('Please confirm your email!', 'warning')
                return redirect(url_for('auth.login'))


            login_user(user, remember=remember)

            return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in!', 'danger')
        return redirect(url_for('main.index'))

    else:
        if request.method == 'GET':
            return render_template('register.html')

        elif request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password = request.form.get('password')
            confirm_password = request.form.get('password_confirm')

            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email address already registered!', 'danger')
                return redirect(url_for('auth.register'))

            if password != confirm_password:
                flash('Password missmatch!', 'danger')
                return redirect(url_for('auth.register'))

            new_user = User(id=None, username=username, first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='sha256'), is_admin=False, is_confirmed=False, phone_number=None)

            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('auth.login'))
            

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))