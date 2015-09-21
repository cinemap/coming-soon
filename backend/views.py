from flask import render_template, request, redirect
from flask.ext.user import login_required, current_user
from sqlalchemy.orm import joinedload

from app import app, db
from models import Film, Person


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@app.route('/')
def index():
    if current_user.is_anonymous():
        return render_template('index.jade')
    else:
        directors = Person.query.filter(Person.followed_by.contains(current_user))
        films = []
        for director in directors:
            query = Film.query.filter(Film.directors.contains(director))
            director_films = query.filter(Film.release_date >= '2014-01-01')
            films.extend(director_films)
        films.sort(key=lambda film: film.release_date)
        films = f7(films)
        return render_template('films.jade', films=films)


@app.route('/film/<pretty_id>')
def film(pretty_id):
    film = Film.query.filter_by(pretty_id=pretty_id).first()
    return render_template('film.jade', film=film)


@app.route('/settings')
@login_required
def settings():
    directors = []
    option = joinedload('director_of').load_only(Film.id)
    for person in Person.query.options(option).all():
        if person.director_of:
            directors.append(person)
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



        