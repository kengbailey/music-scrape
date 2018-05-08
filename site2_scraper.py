'''
    Kenneth Bailey
    5/3/18

    Scraper for undisclosed site #2.

'''

import requests
import re
import sys
import configparser
import datetime
from bs4 import BeautifulSoup
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
            singles = []            
            soup = BeautifulSoup(r.text, "html.parser")
            single = soup.find_all("div", class_="duv")
            for i,al in enumerate(single):   
                temp = {}
                temp['link'] = al.find_all("a")[0]['href']
                temp['single'] = al.find_all("span", class_="title")[0].text
                singles.append(temp)

            if len(singles) > 0:
                return singles
            else:
                print("No albums found on site2!")
                sys.exit(0)

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
            mixtapes = []            
            soup = BeautifulSoup(r.text, "html.parser")
            tapes = soup.find_all("div", class_="duv")
            for i,al in enumerate(tapes):   
                temp = {}
                temp['link'] = al.find_all("a")[0]['href']
                temp['mixtape'] = al.find_all("span", class_="title")[0].text
                mixtapes.append(temp)

            if len(mixtapes) > 0:
                return mixtapes
            else:
                print("No albums found on site2!")
                sys.exit(0)

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
            albums = []            
            soup = BeautifulSoup(r.text, "html.parser")
            album = soup.find_all("div", class_="duv")
            for i,al in enumerate(album):   
                temp = {}
                temp['link'] = al.find_all("a")[0]['href']
                temp['album'] = al.find_all("span", class_="title")[0].text
                albums.append(temp)

            if len(albums) > 0:
                return albums
            else:
                print("No albums found on site2!")
                sys.exit(0)
        
        except Exception as e:
            print("Failed to get albums from site2\n", e)
            sys.exit(0)

    else:
        print("Albums Url fetch failed! Status code: {}".format(r.status_code))
        sys.exit(0)

if __name__ == "__main__":
   
    # run
    singles = getSingles()
    albums = getAlbums()
    mixtapes = getMixtapes()
    conn = connectDb()
    site2RipsToDB(conn, mixtapes)
    site2RipsToDB(conn, albums)
    site2RipsToDB(conn, singles)