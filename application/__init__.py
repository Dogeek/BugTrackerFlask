# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from application.error_handlers import *


from application.mod_main.models import Base
from application.mod_users.models import User
from application.mod_issues.models import Issue, Attachment
from application.mod_comments.models import Comment
# Import a module / component using its blueprint handler variable (mod_auth)

# Build the database:
# This will create the database file using SQLAlchemy

db.create_all()
db.session.commit()

from application.mod_auth.controllers import mod_auth as auth_module
from application.mod_main.controllers import mod_main as main_module
from application.mod_voting.controllers import mod_voting as voting_module
from application.mod_issues.controllers import mod_issues as issues_module
from application.api.controllers import mod_api_1 as api_module
from application.mod_users.controllers import mod_user as user_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(main_module)
app.register_blueprint(voting_module)
app.register_blueprint(api_module)
app.register_blueprint(issues_module)
app.register_blueprint(user_module)
