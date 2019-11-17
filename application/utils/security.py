from itsdangerous import URLSafeTimedSerializer
from .. import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config.ALLOWED_EXTENSIONS
