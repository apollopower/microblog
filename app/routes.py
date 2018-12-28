from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dude'}
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
        'index.html', title='home', user=user, posts=posts
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)