# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect, url_for, \
                  abort

from werkzeug.utils import secure_filename
import os.path
from application import app

# Import module models (i.e. User)
from application.mod_issues.models import Issue, Attachment
# Import module forms
from application.mod_issues.forms import IssueForm
from application import db
from application.utils import allowed_file

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_issues = Blueprint('issues', __name__, url_prefix='/issue')


@mod_issues.route("/new", methods=["GET", "POST"])
def new():
    form = IssueForm(request.form)
    if form.validate_on_submit():
        issue = Issue(name=form.name.data, description=form.description.data, priority=form.priority.data,
                      status=0, version=form.version.data, operating_system=form.operating_system.data,
                      reported_by=session['profile']['user_id'])
        db.session.add(issue)
        db.session.commit()
        file = request.files.get('file')
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            attachment = Attachment(filepath, issue_id=issue.id)
            db.session.add(attachment)
            db.commit()
        flash('Issue successfully submitted!')
        return redirect(url_for('index'))
    return render_template("issues/new_issue.html", new_issue_form=form)


@mod_issues.route("/<int:issue_id>")
def view_issue(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first_or_404()
    return render_template("issues/view_issue.html", issue=issue)
