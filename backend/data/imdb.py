from csv import DictReader


def extract_imdb_ids(path):
    ''' returns set of extracted imdb ids from rating export at path'''
    f = open(path)
    csvreader = DictReader(f)
    imdb_ids = set([])
    for row in csvreader:
        imdb_id = row['const']
        imdb_ids.add(imdb_id)
    return imdb_ids


def correct_ids(potential_ids):
    '''
    >>> correct_ids(['nm11150'])
    None
    >>> correct_ids(['tt1291150'])
    'tt1291150'
    >>> correct_ids(['tt091431'])
    'tt0091431'
    >>> correct_ids(['tt091431', 'tt0091431'])
    'tt0091431'
    >>> correct_ids(['tt1291150', '1291150'])
    'tt1291150'
    >>> correct_ids(['tt1291150', 'nm1331150'])
    'tt1291150'
    '''
    if len(potential_ids) == 1:
        potential_id = potential_ids[0]
        if is_valid(potential_id):
            return potential_id
        else:
            return correct_id(potential_id)
    else:
        for potential_id in potential_ids:
            if is_valid(potential_id):
                return potential_id
        return None


def correct_id(potential_id):
    number = potential_id[2:]
    corrected = 'tt' + '0' + str(number)
    if is_valid(corrected):
        return corrected
    else:
        return None


def is_valid(potential_id):
    '''
    >>> is_valid('tt1291150')
    True
    '''
    if len(potential_id) == 9 and potential_id.startswith('tt'):
        return True
    else:
        return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
