# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from application import db
from application.mod_main.models import Base
import secrets
import hashlib


# Define a User model
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False,
                      unique=True)
    password = db.Column(db.String(256),  nullable=False)
    salt = db.Column(db.String(64), nullable=False)

    # Authorisation Data: role & status
    group = db.Column(db.String(128), nullable=False, default="user")
    strikes = db.Column(db.SmallInteger, nullable=False, default=0)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.salt = secrets.token_hex(8)
        self.password = hashlib.sha256(f"{password}{self.salt}".encode()).hexdigest()

    def __repr__(self):
        return f'<User {self.name}>'

    def check_password(self, password):
        return hashlib.sha256(f"{password}{self.salt}".encode()).hexdigest() == self.password

    def to_dict(self):
        return {"name": self.name,
                "email": self.email,
                "group": self.group,
                "strikes": self.strikes,
                }

    @property
    def get_issues(self):
        from application.mod_issues.models import Issue
        issues = Issue.query.filter_by(reported_by=self.id).all()
        return issues
