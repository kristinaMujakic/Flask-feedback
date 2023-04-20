from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterUserForm(FlaskForm):
    '''Form to register a User'''

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=1, max=20)])

    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=55)])

    email = StringField('Email', validators=[
                        InputRequired(), Email(), Length(max=50)])

    first_name = StringField('First Name', validators=[
                             InputRequired(), Length(max=50)])

    last_name = StringField('Last name', validators=[
                            InputRequired(), Length(max=50)])


class LoginUserForm(FlaskForm):
    '''login User'''

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=1, max=20)])

    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6, max=55)])


class FeedbackForm(FlaskForm):
    '''Add feedback'''

    title = StringField('Title', validators=[InputRequired(), Length(max=100)])

    content = StringField('Feedback', validators=[InputRequired()])


class DeleteUserForm(FlaskForm):
    ''''''
