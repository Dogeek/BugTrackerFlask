import os


# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
username = "dogeek"
password = "admin"
server_ip = "localhost"
# SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@{server_ip}" \
#                           f"/{os.path.join(BASE_DIR, 'bugtracker.postgre')}"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'bugtracker.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "67d2a35fde25a668efbc5083fdab522d36b762d72dc1da2c17b2d249249006e1"

# Secret key for signing cookies
SECRET_KEY = "510823d23bae74a2f58164b578e3fc2a19d220f86668f2349bde86e1b1e7dad4"


SMTP_EMAIL_SERVER = "smtp.gmail.com"
SMTP_EMAIL_SENDER = "my@gmail.com"
SMTP_EMAIL_PASSWORD = "password"

UPLOAD_FOLDER = "/attachments/"
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif', 'log'}
