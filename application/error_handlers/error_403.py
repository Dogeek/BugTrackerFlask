from flask import render_template
from application import app


@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403
