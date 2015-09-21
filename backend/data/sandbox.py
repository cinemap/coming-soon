import freebase
from models import Person


def is_director():
    counter = 0
    for person in Person.query.all():
        if person.director_of:
            counter += 1
            print counter

