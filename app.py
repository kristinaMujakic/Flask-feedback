'''Application that lets users sign up and log in to their own accounts'''

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm, DeleteUserForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///signup_login_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '1608'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)


@app.route('/')
def homepage():
    '''Render homepage'''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''Render a form to register/create a user'''

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(
            username, password, first_name, last_name, email)

        with app.app_context():
            db.session.commit()

        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Provide or handle login'''

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('users/login.html', form=form)

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    '''Logout a user'''

    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>')
def show_user(username):
    '''Display a page for logged in user'''

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteUserForm()

    return render_template("users/show.html", user=user, form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Remove a user and redirect to login'''

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    with app.app_context():
        db.session.delete(user)
        db.session.commit()
    session.pop('username')

    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Display a form to add feedback'''

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )
        with app.app_context():
            db.session.add(feedback)
            db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template('feedback/new.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Display a form to edit feedback"""

    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        with app.app_context():
            db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template('/feedback/edit.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''Delete a specific piece of feedback and redirect'''

    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteUserForm()

    if form.validate_on_submit():
        with app.app_context():
            db.session.delete(feedback)
            db.session.commit()

    return redirect(f"/users/{feedback.username}")
