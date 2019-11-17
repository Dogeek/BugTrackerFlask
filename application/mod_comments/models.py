# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from application import db
from application.mod_main.models import Base

from application.mod_users.models import User
from application.mod_issues.models import Issue, Attachment


# Define a User model
class Comment(Base):
    __tablename__ = 'comments'

    issue_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)

    content = db.Column(db.Text(), nullable=False, default="")
    votes = db.Column(db.Integer(), default=0)

    # New instance instantiation procedure
    def __init__(self, issue_id, user_id, content, attachments):

        self.issue_id = issue_id
        self.user_id = user_id
        self.content = content

    def __repr__(self):
        return f'<Comment {self.id} for issue #{self.issue_id} by user #{self.user_id}>'

    @property
    def attachments(self):
        return [a.permalink for a in Attachment.query.filter_by(comment_id=self.id).all()]

    def get_user(self):
        return User.query.filter_by(id=self.user_id)

    def get_issue(self):
        return Issue.query.filter_by(id=self.issue_id)

    def to_dict(self):
        return {"issue_id": self.issue_id,
                "user_id": self.user_id,
                "content": self.content,
                "attachments": self.attachments}
