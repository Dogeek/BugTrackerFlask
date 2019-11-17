# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect, url_for, \
                  abort

# Import module models (i.e. User)
from application.mod_users.models import User

from application import db


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_user = Blueprint('user', __name__, url_prefix='/user')


@mod_user.route("/<int:user_id>")
def view_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template("users/view_user.html", user=user)
