#!/bin/sh -e

pip install -r requirements.txt
mkdir Data

python WebScraping/get_beer_fast.py
python Munging/raw_to_clean_db.py
python Munging/mongo_to_df.py

