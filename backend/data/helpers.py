import re
import translitcodec
import logging
from collections import Counter

from app import db


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. Taken from http://flask.pocoo.org/snippets/5/"""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def add_pretty_ids(model, base_attribute):
    if not hasattr(model, base_attribute):
        template = '{} has no attribute {} to use for generating pretty ids'
        raise Exception(template.format(model, base_attribute))

    for instance in model.query.all():
        instance.pretty_id = None
    db.session.commit()

    counter = Counter()
    for instance in model.query.all():
        if getattr(instance, base_attribute):
            base = getattr(instance, base_attribute)
        else:
            base = instance.id
        slug = slugify(base)
        if counter[slug] >= 1:
            counter[slug] += 1
            instance.pretty_id = slug + '_' + str(counter[slug])
            logging.info('Non-unique slug: {}.'.format(slug))
        else:
            counter[slug] += 1
            instance.pretty_id = slug
    db.session.commit()