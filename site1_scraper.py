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
import os

config = configparser.ConfigParser()
config.read('config.ini')

URL = config['Site1']['Url']
FILENAME = config['Site1']['Filename']
HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def getSongs():
    
    r = requests.get(URL, headers=HEADER, timeout=5)
    
    if r.status_code == 200:
        
        try:
            songs = re.findall('rows.push\((.+?)\);', r.text)
            
            if songs:
                return songs
            else:
                print("Failed to find any songs on page!")
                sys.exit(0)
        
        except Exception as e:
            print("Failed to regex find songs!\n", e)
            sys.exit(0)

    else:
        print("Url Fetch Failed! Status Code: ", r.status_code)
        sys.exit(0)

def parseSongs(songList):
    
    parsedSongList = []

    try:
        for song in songList:
            x = json.loads(song)
            parsedSongList.append(x)

    except Exception as e:
        print("Failed to parse songs!\n", e)
        sys.exit(0)

    return parsedSongList

def printSong(song):
    
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
    
    try:
        for song in songList:
            print(song['artist'], "-",  song['title'], "(feat. "+song['featuring']+")")
    
    except Exception as e:
        print("Failed to print song info!\n", e)
        sys.exit(0)

def getSongDownloadLink(songUrl):
    
    r.get(songUrl, headers=HEADER, timeout=5)
    
    if r.status_code == 200:
        try:
            
            song = re.findall('download_from_url|(.+?)', r.text)
            print(song)

        except Exception as e:
            print("Failed to find song download url!\n", e)
            sys.exit(0)

    else:
        print("Failed to get song via url:", songUrl)
        sys.exit(0)

def songListToCSV(songList):
   
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
        return os.path.realpath(songData.name)

    except Exception as e:
        print("Failed to create CSV of songs", e)
        sys.exit(0)

def songListToJson(songList):
    
    try:
        tempJson = json.dumps(songList)
        return tempJson
    
    except Exception as e:
        print("Failed to convert songList to Json", e)
        sys.exit(0)

if __name__ == "__main__":
   
    
    songs = getSongs()
    print("# Songs Found: ", len(songs))
    
    parsedSongs = parseSongs(songs)
    
    # save songs locally
    csvPath = songListToCSV(parsedSongs)
    print("CSV Path: ", csvPath)
    
    # songs to json
    jsonSongs = songListToJson(parsedSongs)

    # pretty print json
    #print(json.dumps(firstSong, indent=4, sort_keys=True))
