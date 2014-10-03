import json
import urllib
import logging
from datetime import date


api_key = 'AIzaSyB0wyFuftrrbmKGCyHv0ZE6BsDq6IQraEQ'
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'


def get_result(query):
    params = {
        'query': json.dumps(query),
        'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    try:
        response = json.loads(urllib.urlopen(url).read())
    except Exception as e:
        raise Exception('freebase query problem: ' + str(e))
    if response is None:
        raise Exception
    elif not 'result' in response:
        raise Exception('freebase query problem. query: ' + json.dumps(query))
    else:
        logging.debug('freebase query result downloaded')
        return response['result']


def get_iterative_results(query, limit_per_iteration=1000, limit=100000000):
    ''' deprecated '''
    query['limit'] = limit_per_iteration
    query = [query]
    results = []

    def do_query(cursor=""):
        while True:
            try:
                params = {
                    'query': json.dumps(query),
                    'key': api_key,
                    'cursor': cursor
                }
                url = service_url + '?' + urllib.urlencode(params)
                response = json.loads(urllib.urlopen(url).read())
                break
            except:
                print('Freebase error. (cursor=' + cursor +')')
        results.extend(response['result'])
        return response.get("cursor")

    cursor = do_query()
    iter_counter = 0
    while(cursor):
        iter_counter += 1
        if iter_counter % 10 == 0:
            print('... in iteration ' + str(iter_counter))
        if len(results) >= limit:
            break
        cursor = do_query(cursor)

    return results


def iterate(query, limit_per_iteration=100, limit=-1):

    query['limit'] = limit_per_iteration
    query = [query]
    params = {
        'query': json.dumps(query),
        'key': api_key,
    }
    n_results, iter_counter, cursor = 0, 0 , ''

    while True:
        iter_counter += 1

        if iter_counter % 10 == 0:
            logging.info('Freebase query in iteration {}.'.format(str(iter_counter)))
        params['cursor'] = cursor
        url = service_url + '?' + urllib.urlencode(params)
        try:
            response = json.loads(urllib.urlopen(url).read())
        except:
            raise Exception('Freebase error with query ' + json.dumps(query))

        for result in response['result']:
            n_results += 1
            if limit > 0 and n_results > limit:
                raise StopIteration()
            else:
                yield result
        cursor = response['cursor']
        if not cursor:
            break


def count(type):
    query = {
        'type': type,
        'return': 'count'
    }
    return get_result(query)


def to_date(string):
    ''' converts freebase date string into python date object '''
    parts = string.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    return date(year, month, day)