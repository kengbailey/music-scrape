'''
    Kenneth Bailey
    3/23/18

    Scraper for undisclosed music site #1.

'''

import requests
import re
import sys
import json
import configparser
import csv 
import datetime
from os import path
from db import *
import time

config = configparser.ConfigParser()
config.read('config.ini')

URL = config['Site1']['Url']
FILENAME = config['Site1']['Filename']
HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def getSongs():
    """ Retrieves all songs currently on the first page of Site1."""

    r = requests.get(URL, headers=HEADER, timeout=5)
    
    if r.status_code == 200:
        
        try:
            songs = re.findall('rows.push\((.+?)\);', r.text)                        
            newSongs = [ json.loads(x) for x in songs ]
            if len(newSongs) > 0:
                return newSongs
            else:
                print("Failed to find any songs on page!")
                sys.exit(0)
        
        except Exception as e:
            print("Failed to regex find songs!\n", e)
            sys.exit(0)

    else:
        print("Url Fetch Failed! Status Code: ", r.status_code)
        sys.exit(0)

def printSong(song):
    """ Prints chosen bits of a particular song """

    try:
        print("Title: ", song['title'])
        print("Artist: ", song['artist'])
        if song['featuring']:
            print("Featuring: ", song['featuring'])
        print("Url: ", URL+song['view_url'])

    except Exception as e:
        print("Failed to print song info!\n", e)
        sys.exit(0)

def printSongs(songList):
    """ Prints chosen bits of all songs """

    try:
        for song in songList:
            print(song['artist'], "-",  song['title'], "(feat. "+song['featuring']+")")
    
    except Exception as e:
        print("Failed to print song info!\n", e)
        sys.exit(0)

def getSongDownloadLink(songUrl):
    """ Gets the song download URL of a particular song """

    r.get(songUrl, headers=HEADER, timeout=5)
    
    if r.status_code == 200:
        try:            
            soup = BeautifulSoup(r.text,"html.parser")
            soup_song = soup.find_all("div", class_="jp-progress")            
            realSong = [x for x in soup_song if "url" in str(x)]
            temp = str(realSong).split("|")
            realerSong = [x for x in temp if "mp3" in x][0]
            link = realerSong.split("')")[0]
            return link 

        except Exception as e:
            print("Failed to find song download url!\n", e)
            sys.exit(0)

    else:
        print("Failed to get song via url:", songUrl)
        sys.exit(0)

def songListToCSV(songList):
    """ Outputs all songs to a csv file """

    try:
        datetimePart = datetime.datetime.now().strftime("_%H%M-%m%d%Y")
        filename = FILENAME+datetimePart+".csv"

        songData = open(filename, 'w')

        csvWriter = csv.writer(songData)

        for i, song in enumerate(songList):
            if i == 0:
                header = song.keys()
                csvWriter.writerow(header)
            else:
                csvWriter.writerow(song.values())

        songData.close()
        return path.realpath(songData.name)

    except Exception as e:
        print("Failed to create CSV of songs", e)
        sys.exit(0)

if __name__ == "__main__":
    
    # run
    start = time.time()
    songs = getSongs()
    dbConn = connectDb()
    site1ToDb(dbConn, songs)
    print("Successfully scraped and inserted {} songs into DB!\nTime Elapsed: {}s ".format(len(songs), time.time()-start))

    # save songs locally
    #csvPath = songListToCSV(parsedSongs)
    #print("CSV Path: ", csvPath)

    # pretty print json
    #print(json.dumps(parsedSongs[0], indent=4, sort_keys=True))
