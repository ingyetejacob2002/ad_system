from flask import Blueprint, render_template, request, redirect
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/dashboard')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
