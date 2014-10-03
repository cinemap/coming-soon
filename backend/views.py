from flask import render_template
from main import app
from models import Film
from flask.ext.user import login_required


@app.route('/')
def index():
    films = Film.query.order_by(Film.release_date).all()
    return render_template('index.jade', films=films)


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.jade')
