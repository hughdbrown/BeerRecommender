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
import os

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


if __name__ == '__main__':

    ########
    # Load
    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    MONGO_HOSTNAME = os.environ['MONGO_HOSTNAME']

    # Check server:
    try:
        address = 'mongodb://'
        address += MONGO_USERNAME + ':'
        address += MONGO_PASSWORD + '@'
        address += MONGO_HOSTNAME
        cli = MongoClient(address, serverSelectionTimeoutMS=100)
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

    beer_co_raw = db[raw]
    beer_co_clean = db[clean]

    ########################
    # Process / Write to DB

    # DYLAN: I got 244 pages -> 12200 beers  (though I think it should be 247?)
    # Each document will be one beer:
    for entry in beer_co_raw.find():
        for e in entry['data']:
            beer_co_clean.insert_one(e)
