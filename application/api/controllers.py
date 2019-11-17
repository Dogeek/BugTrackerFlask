from flask import Blueprint, abort, request
import json
from werkzeug.utils import secure_filename
import os.path

from application import db

from application.mod_users.models import User
from application.mod_issues.models import Issue, Attachment
from application.mod_comments.models import Comment
from application.utils import allowed_file

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_api_1 = Blueprint('api', __name__, url_prefix='/api/v1')


@mod_api_1.route("/issues", methods=["GET"])
def get_all_issues():
    issues = [i.to_dict() for i in db.session.query(Issue).all()]
    if not issues:
        abort(404)
    return json.dumps(issues, indent=4), 200


@mod_api_1.route("/issue/<int:issue_id>", methods=["GET"])
def get_issue(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first()
    if issue is None:
        abort(404)
    return json.dumps(issue.to_dict(), indent=4), 200


@mod_api_1.route("/issue/<int:issue_id>/comments", methods=["GET"])
def get_issue_comments(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first()
    if issue is None:
        abort(404)
    comments = Comment.query.filter_by(issue_id=issue_id).all()
    if not comments:
        return json.dumps([], indent=4), 200
    return json.dumps([c.to_dict() for c in comments], indent=4), 200


@mod_api_1.route("/users", methods=["GET"])
def get_all_users():
    users = db.session.query(User).all()
    if not users:
        return '[]', 200
    return json.dumps([u.to_dict() for u in users], indent=4), 200


@mod_api_1.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return json.dumps(user.to_dict(), indent=4), 200


@mod_api_1.route("/issue/new", methods=["POST"])
def new_issue():
    form = request.form
    required_keys = ["name", "priority", "version", "operating_system", "reported_by"]
    for k in required_keys:
        if k not in form.keys():
            abort(400)
    name = form["name"]
    description = form.get("description", "")
    priority = form.get("priority")
    status = form.get("status", 0)
    version = form.get("version")
    operating_system = form.get("operating_system")
    reported_by = form.get("reported_by")
    issue = Issue(name=name, description=description, priority=priority,
                  status=status, version=version, operating_system=operating_system,
                  reported_by=reported_by)
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
    return "", 200
