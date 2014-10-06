from flask import render_template
from main import app, mail
from models import Film, Person
from flask.ext.user import login_required
from flask.ext.mail import Message


@app.route('/')
def index():
    films = Film.query.order_by(Film.release_date).all()
    return render_template('index.jade', films=films)


@app.route('/settings')
@login_required
def settings():
    directors = Person.query.filter(Person.director_of.any()).all()
    return render_template('settings.jade', directors=directors)



        