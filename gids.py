import csv

def get_gids(path='/data/gids.csv'):
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        gids = list(reader)
    return gids