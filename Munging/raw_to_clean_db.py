''' Authors: Dylan Albrecht
             Trent Woodbury

    Date: December 17, 2016

    Takes MongoDB collection 'craft_beers_raw' generated by get_beers_fast.py
    to MongoDB collection 'craft_beers'

    NOTE: Each beer is a dictionary entry, descriptions are found in
          entry['description']  and
          entry['style']['description']

'''
import sys

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


if __name__ == '__main__':

    ########
    # Load

    # Check server:
    try:
        cli = MongoClient(serverSelectionTimeoutMS=10)
        cli.server_info()

    except ServerSelectionTimeoutError as e:
        print "Server error!  (Is it plugged in?): "
        print e
        raise e
    
    raw = 'craft_beers_raw'
    clean = 'craft_beers'

    db = cli['beer_db']
    cols = db.collection_names()

    # Check for collections:
    if raw not in cols:
        print raw + ' does not exists yet! Run web-scraper first!'
        sys.exit()

    if clean in cols:
        print clean + ' already exists! Check or drop.'
        sys.exit()

    beer_co_raw = db['craft_beers_raw']
    beer_co_clean = db['craft_beers']

    ###########
    # Process

    # DYLAN: I got 244 pages -> 12200 beers
    # Each document will be one beer:
    for entry in beer_co_raw.find():
        for e in entry['data']:
            beer_co_clean.insert_one(e)


