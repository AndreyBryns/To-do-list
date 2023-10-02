from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Incorrect login or password.')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('main.home'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')

    if User.query.filter_by(email=email).first():
        flash('A user with this email address already exists.')
        return render_template('signup.html')

    new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2'))

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))