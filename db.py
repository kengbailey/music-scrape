"""
    Kenneth Bailey
    4/23/18

    Notes:

"""

import psycopg2
import os
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DBNAME = config['DB']['DbName']
USER = config['DB']['User']
HOST = config['DB']['Host']
PW = config['DB']['Password']

# insertion sql queries
SITE1SQLQUERY = '''
insert into ddrip.rawdailyrips(amazon, artist, create_time,
                                song_desc, dislikes, download_block,
                                download_url, featuring, file, full_artist,
                                google, image, itunes, likes, live_time,
                                live_time_day, live_time_f, priority, rating,
                                secondary_title, thumb_56, thumb_url, thumb_video,
                                title, song_type, update_time, url, view_url,
                                view_mobile_url, views, site_id, num)
values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

SITE2QUERY_SINGLES = '''
insert into nineclacks.rawsingle(name, link)
values (%s, %s)
'''

SITE2QUERY_ALBUMS = '''
insert into nineclacks.rawalbum(name, link)
values(%s, %s)
'''

SITE2QUERY_MIXTAPES = '''
insert into nineclacks.rawmixtape(name, link)
values(%s, %s)
'''

def connectDb():
    try:
        conn_str = "dbname={} user={} host={} password={}".format(DBNAME, USER, HOST, PW)
        conn = psycopg2.connect(conn_str)
        print("Successfully connected to db!")
        return conn

    except Exception as e:
        print("Failed to connect to db!", e)

def site1ToDb(conn, songList):
    num = None
    try:
        # get rip num
        with conn.cursor() as cur:
            cur.execute("select num from ddrip.rawdailyrips order by id desc limit 1")
            one = cur.fetchone()
            num = int(one[0])+1

        # execute sql query                
        for song in songList:
            with conn.cursor() as cur:
                cur.execute(SITE1SQLQUERY, (song['amazon'], song['artist'], song['create_time'], song['desc'],
                                    song['dislikes'], song['download_block'], song['download_url'], 
                                    song['featuring'], song['file'], song['full_artist'], song['google'],
                                    song['image'], song['itunes'], song['likes'], song['live_time'],
                                    song['live_time_day'], song['live_time_f'], song['priority'],
                                    song['rating'], song['secondary_title'], song['thumb_56'],
                                    song['thumb_url'], song['thumb_video'], song['title'], song['type'],
                                    song['update_time'], song['url'], song['view_url'], song['view_mobile_url'],
                                    song['views'],song['id'], num))
                conn.commit()

        print("Successfully inserted {} songs!".format(len(songList)))                

    except Exception as e:
        print("Failed to insert all songs! -->", e)

if __name__ == "__main__":  
    
    # run
    conn = connectDb()
    cur = conn.cursor()
    cur.execute("select * from ddrip.rawdailyrips order by id desc limit 1")
    one = cur.fetchone()
    conn.close()
    print(one)
