# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect, url_for, \
                  abort

# Import module models (i.e. User)
from application.mod_users.models import User

# Import module forms
from application.mod_auth.forms import LoginForm, SignupForm, EmailForm, PasswordForm

from application import db

from application.utils import send_email, ts

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))
        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", signin_form=form)


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('index'))

    return render_template('auth/signup.html', signup_form=form)


@mod_auth.route('/forgot', methods=["GET", "POST"])
def forgot():
    form = EmailForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"

        # Here we use the URLSafeTimedSerializer
        token = ts.dumps(user.email, salt='recover-key')

        reset_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/reset.html',
            reset_url=reset_url)

        send_email(user.email, subject, html)

        return redirect(url_for('index'))

    return render_template('auth/forgot.html', forgot_form=form)


@mod_auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin'))

    return render_template('auth/reset.html', form=form, token=token)
