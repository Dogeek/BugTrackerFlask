# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField  # BooleanField

# Import Form validators
from wtforms.validators import DataRequired, Email, NoneOf

from application.mod_users.models import User


# Define the login form (WTForms)
class LoginForm(FlaskForm):
    email = StringField('Email Address', [Email(),
                        DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                             DataRequired(message='Must provide a password.')])


class SignupForm(FlaskForm):
    email = StringField('Email Address', [Email(), DataRequired(message="An email is required")])
    password = PasswordField('Password', [DataRequired(message='Must provide a password.')])
    username = StringField('Username', [DataRequired(), NoneOf([u.name for u in User.query.all()],
                                                               message="This username is already in use.")])


class EmailForm(FlaskForm):
    email = StringField('Email Address', [Email(), DataRequired(message="An email is required")])


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
