import freebase

query = {
    'type': '/film/film',
    'mid': '/m/0y88_95',
    'initial_release_date': None
}

result = freebase.get_result(query)
date = result['initial_release_date']
print type(date), date
