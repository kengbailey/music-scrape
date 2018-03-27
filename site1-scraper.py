'''
    Kenneth Bailey
    3/23/18

    Scraper for an undisclosed music site.

'''

import requests
import re
import sys
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

URL = config['Site']['Url']
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

def printSongInfo(song):
    
    try:
        print("Title: ", song['title'])
        print("Artist: ", song['artist'])
        if song['featuring']:
            print("Featuring: ", song['featuring'])
        print("Url: ", URL+song['view_url'])
    except Exception as e:
        print("Failed to pring song info!\n", e)
        sys.exit(0)

if __name__ == "__main__":
    
    songs = getSongs()
    print("# Songs Found: ", len(songs))
    
    parsedSongs = parseSongs(songs)

    printSongInfo(parsedSongs[0])

