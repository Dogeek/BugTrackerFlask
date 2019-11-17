# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SelectField
from wtforms.fields import TextAreaField

# Import Form validators
from wtforms.validators import DataRequired

from application.mod_issues.models import Priorities, OperatingSystems


# Define the login form (WTForms)
class IssueForm(FlaskForm):
    name = StringField('Name', [DataRequired(message='Issue must have a name')])
    priority = SelectField('Priority', choices=list(zip(range(len(Priorities.PRIORITIES)), Priorities.PRIORITIES)))
    operating_system = SelectField('OS', choices=list(zip(range(len(OperatingSystems.OSES)), OperatingSystems.OSES)))
    version = StringField("Version", [DataRequired()])
    attachments = FileField("Attach a file")
    description = TextAreaField("Description")
