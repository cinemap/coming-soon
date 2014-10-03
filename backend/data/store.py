import inspect
import logging

from sqlalchemy.orm import joinedload, subqueryload
import sys
import os
BACKEND_DIR = os.environ['BASEDIR'] + '/backend'
sys.path.append(BACKEND_DIR)
# import main
from models import Film, Person, Language, Country
import models
from main import db


class Store(object):

    def __init__(self):
        self.dict = dict()
        self.initiated_models = set([])
        for __, model in inspect.getmembers(models, inspect.isclass):
            self.dict[model] = dict()

    def _init_model(self, model):
        logging.info('initiating store for model {}...'.format(model))

        options = []
        if model == Film:
            options = [
                subqueryload(Film.directors).load_only(Person.id),
                subqueryload(Film.actors).load_only(Person.id),
                subqueryload(Film.languages).load_only(Language.id),
                subqueryload(Film.production_countries).load_only(Country.id)
            ]
        instances = model.query.options(*options).all()
        for instance in instances:
            self.dict[model][instance.id] = instance
        logging.info('...done.')
        self.initiated_models.add(model)

    def get(self, model, id):
        if model not in self.initiated_models:
            self._init_model(model)
        if id in self.dict[model]:
            return self.dict[model][id]
        else:
            instance = model(id=id)
            db.session.add(instance)
            self.dict[model][id] = instance
            return instance
