from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.models import User
from app import app, db
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Jonas'},
            'body': 'Rainy day in Miami!'
        },
        {
            'author': {'username': 'Snorlax'},
            'body': 'I ate too much Guava Cheesecake'
        }
    ]
    return render_template(
        'index.html', title='home', posts=posts
        )

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Edge Case: User already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    # Handling POST Request
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    # GET Request
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Edge Case: User is already Logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    # POST Request
    if form.validate_on_submit():
        # Look for user
        user = User.query.filter_by(username=form.username.data).first()
        # Check if user exists or if password doest not match
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        # User is authenticated, log in and create session
        # Redirects user to the next page
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    # GET Request
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))