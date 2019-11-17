from flask import render_template
from application import app


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404
