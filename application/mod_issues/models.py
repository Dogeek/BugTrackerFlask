# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from application import db
from application.mod_users.models import User
from application.mod_main.models import Base


class Statuses:
    WAITING = 0
    STARTED = 1
    IN_PROGRESS = 2
    DONE = 3

    STATUSES = ["WAITING", "STARTED", "IN_PROGRESS", "DONE"]

    @classmethod
    def to_string(cls, status):
        if isinstance(status, int):
            return cls.STATUSES[status]
        elif isinstance(status, str):
            return status
        else:
            raise TypeError()


class Priorities:
    URGENT = 0
    MAJOR = 1
    MEDIUM = 2
    MINOR = 3

    PRIORITIES = ["URGENT", "MAJOR", "MEDIUM", "MINOR"]

    @classmethod
    def to_string(cls, priority):
        if isinstance(priority, int):
            return cls.PRIORITIES[priority]
        elif isinstance(priority, str):
            return priority
        else:
            raise TypeError()


class OperatingSystems:
    WINDOWS = 0
    MACOS = 1
    LINUX = 2
    ANDROID = 3
    IOS = 4
    OTHER = 5

    OSES = ["WINDOWS", "MACOS", "LINUX", "ANDROID", "IOS", "OTHER"]

    @classmethod
    def to_string(cls, os):
        if isinstance(os, int):
            return cls.OSES[os]
        elif isinstance(os, str):
            return os
        else:
            raise TypeError()


# Define a User model
class Issue(Base):
    __tablename__ = 'issues'
    __table_args__ = {'sqlite_autoincrement': True}

    # Issue name & description
    name = db.Column(db.String(128),  nullable=False)
    description = db.Column(db.Text(convert_unicode=True),  nullable=True)

    # Issue status (in progress, in dev, not fixing etc) and priority (urgent, major, medium, minor)
    status = db.Column(db.Integer(),  nullable=False)
    priority = db.Column(db.Integer(), nullable=False)
    version = db.Column(db.String(128), nullable=False)
    votes = db.Column(db.Integer(), default=0)
    operating_system = db.Column(db.Integer(), default=0)

    # User ID that reported the issue
    reported_by = db.Column(db.BigInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, description, status, priority, version, operating_system, reported_by):

        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.version = version
        self.operating_system = operating_system
        self.reported_by = reported_by.id

    def __repr__(self):
        status = Statuses.to_string(self.status)
        priority = Priorities.to_string(self.priority)
        return f'<Issue {self.name} {self.description} {status} {priority}>'

    @property
    def status_string(self):
        return Statuses.to_string(self.status)

    @property
    def os_string(self):
        return OperatingSystems.to_string(self.operating_system)

    @property
    def priority_string(self):
        return Priorities.to_string(self.priority)

    @property
    def reported_by_name(self):
        return User.query.filter_by(id=self.reported_by).first().name

    def values(self):
        status = Statuses.to_string(self.status)
        priority = Priorities.to_string(self.priority)
        reported_by = User.query.filter_by(id=self.reported_by).first().name
        operating_system = OperatingSystems.to_string(self.operating_system)
        return [self.name, status, priority, reported_by, self.version, operating_system]

    @staticmethod
    def columns():
        return ["Name", "Status", "Priority", "Reported by", "Version", "Operating system"]

    @property
    def attachments(self):
        return [a.permalink for a in Attachment.query.filter_by(issue_id=self.id).all()]

    def to_dict(self):
        dct = {k: v for k, v in zip(self.columns(), self.values())}
        dct["attachments"] = self.attachments
        return dct


class Attachment(Base):
    __tablename__ = 'attachments'
    __table_args__ = {'sqlite_autoincrement': True}

    permalink = db.Column(db.String(128), nullable=False)
    issue_id = db.Column(db.Integer(), nullable=True)
    comment_id = db.Column(db.Integer(), nullable=True)

    def __init__(self, permalink, issue_id=None, comment_id=None):
        if comment_id is None and issue_id is None:
            raise ValueError("Exception on Attachment class, issue_id or comment_id must be provided.")

        if comment_id is not None and issue_id is not None:
            raise ValueError("Exception on Attachment class, issue_id and comment_id can't be both specified.")

        self.permalink = permalink
        self.issue_id = issue_id
        self.comment_id = comment_id

    def get_attached_id(self):
        return ("issue", self.issue_id) if self.issue_id is not None else ("comment", self.comment_id)
