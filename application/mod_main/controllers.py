# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect

from application import db
from application.mod_issues.models import Issue
from application.mod_auth.forms import LoginForm
from application.mod_users.models import User


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_main = Blueprint('main', __name__, url_prefix='')


@mod_main.route("/", methods=["GET", "POST"])
def index():
    issues = [Issue.columns()] + db.session.query(Issue).all()
    # If sign in form is submitted
    signin_form = LoginForm(request.form)
    # Verify the sign in form
    if signin_form.validate_on_submit():
        user = User.query.filter_by(email=signin_form.email.data).first()
        if user and user.check_password(signin_form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect("/")
        flash('Wrong email or password', 'error-message')
    return render_template("index.html", issues=issues, signin_form=signin_form)

