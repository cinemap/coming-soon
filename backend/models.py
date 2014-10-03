from datetime import date

from sqlalchemy.orm import load_only
from flask import g
from flask.ext.user import UserMixin

from main import db

trailer_table = db.Table(
    'trailer',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('video_id', db.Text, db.ForeignKey('video.id')))

main_country_of_language_table = db.Table(
    'main_country_of_language',
    db.Column('language_id', db.Text, db.ForeignKey('language.id')),
    db.Column('country_id', db.Text, db.ForeignKey('country.id')))

production_country_table = db.Table(
    'production_country',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('country_id', db.Text, db.ForeignKey('country.id')))

nationality_table = db.Table(
    'nationality',
    db.Column('person_id', db.Text, db.ForeignKey('person.id')),
    db.Column('country_id', db.Text, db.ForeignKey('country.id')))

place_country_table = db.Table(
    'place_country',
    db.Column('place_id', db.Text, db.ForeignKey('place.id')),
    db.Column('country_id', db.Text, db.ForeignKey('country.id')))

film_country_table = db.Table(
    'film_country',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('country_id', db.Text, db.ForeignKey('country.id')))

film_language_table = db.Table(
    'film_language',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('language_id', db.Text, db.ForeignKey('language.id')))

director_table = db.Table(
    'director',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('person_id', db.Text, db.ForeignKey('person.id')))

actor_table = db.Table(
    'actor',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('person_id', db.Text, db.ForeignKey('person.id')))

official_language_table = db.Table(
    'official_language',
    db.Column('country_id', db.Text, db.ForeignKey('country.id')),
    db.Column('language_id', db.Text, db.ForeignKey('language.id')))

spoken_in_table = db.Table(
    'spoken_in',
    db.Column('country_id', db.Text, db.ForeignKey('country.id')),
    db.Column('language_id', db.Text, db.ForeignKey('language.id'))
)

in_collection_table = db.Table(
    'in_collection',
    db.Column('film_id', db.Text, db.ForeignKey('film.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, default='')


class Film(db.Model):
    id = db.Column(db.Text, primary_key=True)
    freebase_mid = db.Column(db.Text, unique=True)
    imdb_id = db.Column(db.Text, unique=True)
    tmdb_id = db.Column(db.Integer, unique=True)
    pretty_id = db.Column(db.Text, unique=True)

    title_original = db.Column(db.Text)
    title_de = db.Column(db.Text)
    title_en = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    release_date = db.Column(db.Date)
    small_poster_url = db.Column(db.Text)
    tmdb_poster = db.Column(db.Text)
    popularity = db.Column(db.Float)

    actors = db.relationship(
        'Person',
        secondary=actor_table,
        backref=db.backref('acted_in', lazy='dynamic'))

    directors = db.relationship(
        'Person',
        secondary=director_table,
        backref=db.backref('director_of')
    )

    languages = db.relationship(
        'Language',
        secondary=film_language_table,
        backref=db.backref('films')
    )

    production_countries = db.relationship(
        'Country',
        secondary=production_country_table,
        backref=db.backref('production_country_of')
    )

    countries = db.relationship(
        'Country',
        secondary=film_country_table,
        backref=db.backref('films', lazy='dynamic')
    )

    trailers = db.relationship(
        'Video',
        secondary=trailer_table,
        backref=db.backref('trailer_of')
    )

    collections = db.relationship(
        'Collection',
        secondary=in_collection_table,
        backref=db.backref('films')
    )

    @property
    def popular_actors(self):
        return Person.query.\
            filter(Person.acted_in.contains(self)).\
            order_by(Person.actor_popularity.desc())[0:5]

    def title(self, locale):
        attr = 'title_{}'.format(locale)
        return getattr(self, attr)

    def main_title(self, locale):
        if self.title(locale):
            return self.title(locale)
        elif self.title_original:
            return self.title_original
        else:
            return self.title('en')

    def secondary_title(self, locale):
        if self.main_title(locale) == self.title(locale) and self.title_original != self.title(locale):
            return self.title_original

    def __repr__(self):
        return '<%r>' % self.id

class Country(db.Model):

    id = db.Column(db.Text, primary_key=True)
    freebase_mid = db.Column(db.Text, unique=True)
    pretty_id = db.Column(db.Text, unique=True)
    iso_3166_1_numeric = db.Column(db.String(3))


    name_de = db.Column(db.Text)
    name_en = db.Column(db.Text)
    capital_id = db.Column(db.Text, db.ForeignKey('place.id'))
    population = db.Column(db.Integer)

    def name(self, language):
        attribute = 'name_{}'.format(language)
        return getattr(self, attribute)

    @property
    def popular_directors(self):
        option = load_only(Person.id, Person.pretty_id, Person.name)
        query = Person.query.options(option)
        query = query.filter(Person.nationalities.contains(self))
        query = query.order_by(Person.director_popularity.desc())
        return query[0:8]


    def __repr__(self):
        return '<%r>' % self.id

class Place(db.Model):
    id = db.Column(db.Text, primary_key=True)
    freebase_mid = db.Column(db.Text, unique=True)

    name_en = db.Column(db.Text)
    name_de = db.Column(db.Text)

    capital_of = db.relationship('Country', backref='capital')

    countries = db.relationship(
        'Country',
        secondary=place_country_table,
        lazy='joined',
        backref=db.backref('places', lazy='dynamic')
    )


    def __repr__(self):
        return '<%r>' % self.id

class Person(db.Model):
    id = db.Column(db.Text, primary_key=True)
    freebase_mid = db.Column(db.Text, unique=True)
    pretty_id = db.Column(db.Text, unique=True)

    name = db.Column(db.Text)
    tmdb_image = db.Column(db.Text)

    day_of_birth = db.Column(db.Date)
    director_popularity = db.Column(db.Float)
    actor_popularity = db.Column(db.Float)
    homepage = db.Column(db.Text)

    place_of_birth_id = db.Column(db.Text, db.ForeignKey('place.id'))
    place_of_birth = db.relationship(
        'Place',
        backref=db.backref('place_of_birth_of')
    )

    nationalities = db.relationship(
        'Country',
        secondary=nationality_table,
        backref=db.backref('nationality_of')
    )

    @property
    def age(self):
        today = date.today()
        born = self.day_of_birth
        try:
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def __repr__(self):
        return '<%r>' % self.id

class Language(db.Model):
    id = db.Column(db.Text, primary_key=True)
    freebase_mid = db.Column(db.Text, unique=True)

    name_de = db.Column(db.Text)
    name_en = db.Column(db.Text)

    main_countries = db.relationship(
        'Country',
        secondary=main_country_of_language_table,
        backref=db.backref('main_country_of_language')
    )

    official_language_in_countries = db.relationship(
        'Country',
        secondary=official_language_table,
        backref=db.backref('official_languages')
    )

    spoken_in_countries = db.relationship(
        'Country',
        secondary=spoken_in_table,
        backref=db.backref('spoken_languages')
    )


    def __repr__(self):
        return '<%r>' % self.id

class Video(db.Model):
    id = db.Column(db.Text, primary_key=True)
    youtube_id = db.Column(db.Text)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
