from collections import Counter
import logging

import tmdb3

import imdb
import freebase
from store import Store
from app import db
from models import Person, Film, Video
from helpers import add_pretty_ids
TMDB_KEY = '95a5e0f59034242b05d55145c16a1c35'


def add_pretty_ids_to_films():
    add_pretty_ids(Film, 'title_en')


def prototype_import():
    import_directors_from_ratings()
    complete_director_data()
    complete_film_data()
    complete_tmdb_data()


def import_directors_from_ratings():
    path = '/Users/dominic/projects/stan/data/ratings.csv' 
    imdb_ids = imdb.extract_imdb_ids(path)
    store = Store()
    counter = 0
    for imdb_id in imdb_ids:
        counter += 1
        print 'film {}'.format(counter)
        query = {
            'type': '/film/film',
            'key': [{
                'namespace': '/authority/imdb/title',
                'value': imdb_id
            }],
            'directed_by': [{
                'mid': None,
                'optional': 'optional'
            }]
        }
        result = freebase.get_result(query)
        if result:
            for director in result['directed_by']:
                person = store.get(Person, director['mid'])
    db.session.commit()


def complete_person_data():

    store = Store()
    counter = 0
    for person in Person.query.all():
        if person.director_of:  # person has directed at least
            query = {
                'mid': person.id,
                'name': None,
                '/film/director/film': [{
                    'mid': None,
                    # '/film/film/initial_release_date>': '2014-01-01',  
                    'optional': 'optional'
                }] 
            }
            result = freebase.get_result(query)
            person.name = result['name']
            for film in result['/film/director/film']:
                film = store.get(Film, film['mid'])
                person.director_of.append(film) 

            counter += 1
            print counter
    
    db.session.commit()


def complete_film_data():
    store = Store()
    counter = 0
    for film in Film.query.all():
        query = {
            'type': '/film/film',
            'mid': film.id,
            'initial_release_date': None,
            'a:key': [{
                'namespace': '/authority/imdb/title',
                'value': None,
                'optional': 'optional'
            }],
            'b:key': [{
                'namespace': '/wikipedia/en',
                'value': None,
                'optional': 'optional'
            }],
            'name': [{
                'value': None,
                'lang': None,
                'lang|=': ['/lang/de', '/lang/en']
            }],
            'directed_by': [{
                'mid': None,
                'optional': 'optional'
            }],
            'starring': [{
                'actor': {
                    'mid': None
                },
                'optional': 'optional'
            }]
        }
        
        result = freebase.get_result(query)

        if not result:
            print 'problem with {}'.format(film.id)
            continue

        try:
            film.release_date = freebase.to_date(result['initial_release_date'])   
        except Exception, e:
            print 'problem with release date in film {}: {}'.format(result['mid'], result['initial_release_date'])
          
        potential_imdb_ids = [key['value'] for key in result['a:key']]
        film.imdb_id = imdb.correct_ids(potential_imdb_ids)

        for name in result['name']:
            if name['lang'] == '/lang/en':
                film.title_en = name['value']
            if name['lang'] == '/lang/de':
                film.title_de = name['value']

        film.directors = []
        for director in result['directed_by']:
            person = store.get(Person, director['mid'])
            film.directors.append(person)

        film.actors = []
        for performance in result['starring']:
            mid = performance['actor']['mid']
            person = store.get(Person, mid)
            film.actors.append(person)

        counter += 1
        if counter == 5:
            db.session.commit()
        if film.title_en:
            title = film.title_en
        else:
            title = 'no title'
        print 'film {}: {}'.format(counter, title.encode('utf-8')) 

    db.session.commit()


def complete_tmdb_data():
    tmdb3.set_key(TMDB_KEY)
    films = Film.query.all()

    store = Store()
    counter = 0
    for film in films:
        counter += 1
        if counter % 1000 == 0:
            print '{} queries to the movie database done.'.format(counter)
            db.session.commit()
        try:
            result = tmdb3.Movie.fromIMDB(film.imdb_id)
        except:
            logging.warning('Problem with tmdb query with {}.'.format(film))
            continue

        film.tmdb_id = result.id
        film.title_original = result.originaltitle
        film.description_en = result.overview

        # if type(result.releasedate) == datetime.date:
            # film.release_date = result.releasedate
        # else:
            # logging.warning('No usable release date found for {}.'.format(film))

        poster = result.poster
        if poster:
            for size in poster.sizes():
                if size != 'w92':
                    film.small_poster_url = poster.geturl(size)
                    break

        for trailer in result.youtube_trailers:
            youtube_id = trailer.source
            id = 'yt/' + youtube_id
            video = store.get(Video, id)
            video.youtube_id = youtube_id
            film.trailers.append(video)

    db.session.commit()