from flask import render_template, request, redirect
from flask.ext.user import login_required, current_user

from main import app, db
from models import Film, Person


@app.route('/')
def index():
    # TODO correct!!!
    directors = Person.query.filter(Person.followed_by.contains(current_user))
    all_films = Film.query.order_by(Film.release_date).all()
    films = []
    for film in all_films:
        if film.directors[0] in directors:
            films.append(film)
    return render_template('index.jade', films=films)


@app.route('/settings')
@login_required
def settings():
    directors = Person.query.filter(Person.director_of.any()).all()
    return render_template('settings.jade', directors=directors)


@app.route('/save-settings', methods=['POST'])
@login_required
def save_settings():
    followed_directors = []
    for director_id, _ in request.form.iteritems():
        director = Person.query.get(director_id)
        followed_directors.append(director)
    current_user.followed_directors = followed_directors
    db.session.commit()
    return redirect('/')



        