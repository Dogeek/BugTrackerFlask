# Import flask dependencies
from flask import Blueprint

from application.mod_issues.models import Issue

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_voting = Blueprint('voting', __name__, url_prefix='/voting')


@mod_voting.route("/upvote/<int:issue_id>", methods=["POST"])
def upvote(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first()
    issue.votes += 1
    return "200"


@mod_voting.route("/downvote/<int:issue_id>", methods=["POST"])
def downvote(issue_id):
    issue = Issue.query.filter_by(id=issue_id).first()
    issue.votes -= 1
    return "200"
