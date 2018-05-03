'''
    Kenneth Bailey
    5/3/18

    Scraper for undisclosed site #2.

'''

import requests
import re
import sys
import json
import configparser
import datetime
from db import *
import time

config = configparser.ConfigParser()
config.read('config.ini')

SINGLES_URL = config['Site2']['Url_Singles']
MIXTAPES_URL = config['Site2']['Url_Mixtapes']
ALBUMS_URL = config['Site2']['Url_Albums']
HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def getSingles():
    """ Retrieves the singles from page1 of site2 """

    r = requests.get(SINGLES_URL, headers=HEADER, timeout=5)

    if r.status_code == 200:

        try:
            songs = None
            

            return songs

        except Exception as e:
            print("Failed to get Singles from site2\n", e)
            sys.exit(0)

    else:
        print("Singles Url fetch failed! Status code: {}".format(r.status_code))
        sys.exit(0)

def getMixtapes():
    """ Retrieves the mixtapes from page1 of Site2 """
    
    r = requests.get(MIXTAPES_URL, headers=HEADER, timeout=5)

    if r.status_code == 200:

        try:
            mixtapes = None

            return mixtapes

        except Exception as e:
            print("Failed to get mixtapes from site2\n", e)
            sys.exit(0)

    else:
        print("Mixtapes Url fetch failed! Status code: {}".format(r.status_code))
        sys.exit(0)

def getAlbums():
    """ Retrieves the albums from page1 of site2 """

    r = requests.get(ALBUMS_URL, headers=HEADER, timeout=5)

    if r.status_code == 200:
        
        try:
            albums = None

            return albums
        
        except Exception as e:
            print("Failed to get albums from site2\n", e)
            sys.exit(0)

    else:
        print("Albums Url fetch failed! Status code: {}".format(r.status_code))
        sys.exit(0)

if __name__ == "__main__":
   
   # run
   print(getAlbums())
