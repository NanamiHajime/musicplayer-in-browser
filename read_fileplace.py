import sqlite3
import os
import glob
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3

def connect_db():
    HERE_DIR = os.path.dirname(os.path.abspath(__file__))

    dbpath = os.path.join(HERE_DIR, "musics.sqlite")

    # create db or connect
    conn = sqlite3.connect(dbpath, check_same_thread=False, isolation_level=None)
    cur = conn.cursor()
    return cur, conn

def create_db():
    cur=connect_db()[0]
    cur.execute(
        "CREATE TABLE musics(id INTEGER PRIMARY KEY AUTOINCREMENT, album STRING, title STRING, artist STRING, tracknumber INTEGER,total_tracknumber INTEGER, genre, file_place STRING UNIQUE, time_min INTEGER, time_sec INTEGER)"
    )

    cur.close()

# return parameter's extension example:m4a


def return_extension(file_path):
    file_extension = os.path.splitext(file_path)[1][1:]

    return file_extension


# read "music" folder
def read_musicfile():
    music_files=[]
    # read file_
    types=["m4a", "mp3"]
    
    for t in types:
        path_music = "./music/**/*."+t
        music_files=music_files+glob.glob(path_music, recursive=True)
    music_files = [f.replace("\\", "/") for f in music_files]

    return music_files


# insert music data in the database
def insert_musicdata(data_music):
    cur=connect_db()[0]
    conn=connect_db()[1]

    sql = "INSERT INTO musics(album, title, artist, tracknumber, total_tracknumber, genre, file_place, time_min, time_sec) values(?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (file_place) DO NOTHING"
    data = [(
        data_music["album"],
        data_music["title"],
        data_music["artist"],
        data_music["tracknumber"],
        data_music["total_tracknumber"],
        data_music["genre"],
        data_music["file_place"],
        data_music["time_min"],
        data_music["time_sec"]
    )]
    cur.executemany(sql, data)
    conn.commit()

# get music data with mutagen


def get_musicdata_mp3(music_filepath):
    tags = EasyID3(music_filepath)
    music_time = MP3(music_filepath).info.length

    data_music = {"album": tags["album"][0],
                  "title": tags["title"][0],
                  "artist": tags["artist"][0],
                  # tracknumber is like 5/7
                  "tracknumber": tags["tracknumber"][0].split("/")[0],
                  "total_tracknumber": tags["tracknumber"][0].split("/")[1],

                  "genre": tags["genre"][0],
                  "file_place": music_filepath,
                  #time is sec
                  "time_min": int(music_time/60),
                  "time_sec": int(music_time % 60)
                  }

    return data_music


def get_musicdata_m4a(music_filepath):
    mp4 = MP4(music_filepath)
    music_time = mp4.info.length
    track_number = mp4.tags["trkn"]

    data_music = {"album": mp4.tags["\xa9alb"][0],
                  "title": mp4.tags["\xa9nam"][0],
                  "artist": mp4.tags["\xa9ART"][0],
                  # tracknumber is like 5/7
                  "tracknumber": track_number[0][0],
                  "total_tracknumber": track_number[0][1],

                  "genre": mp4.tags["\xa9gen"][0],
                  "file_place": music_filepath,
                  #time is sec
                  "time_min": int(music_time/60),
                  "time_sec": int(music_time % 60)
                  }

    return data_music

'''
https://compute-cucco.hatenablog.com/entry/2019/07/21/204512
'''

def get_count():
    table_name="musics"
    cur=connect_db()[0]
    sql_count="SELECT COUNT (*) FROM {0}".format(table_name)
    #d is like (100, )
    d=cur.execute(sql_count).fetchone()
    cur.close()
    return d[0]

def get_one_column_data_list(table_name, column_name,target_column_index=0):
    #行：row number
    data_size=get_count()
    data_list=[None]*data_size

    sql_select="SELECT {0} FROM {1}".format(column_name,table_name)

    cur=connect_db()[0]
    d=cur.execute(sql_select)

    for index, row in enumerate(d):
        data_list[index]=row[target_column_index]
    cur.close()

    return data_list

#debug
"""
con=sqlite3.connect("musics.sqlite")
data_list=get_one_column_data_list(con, )
print(data_list)

#CHECK DATABASE
cur=connect_db()[0]
cur.execute("SELECT * FROM musics")
"""