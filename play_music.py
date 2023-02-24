import streamlit as st
import os
import read_fileplace
from pydub import AudioSegment

#return parameter's extension example:m4a
def return_extension(file_path):
    file_extension=os.path.splitext(file_path)[1][1:]

    return file_extension
#insert database
def read_database():
    paths_music=read_fileplace.read_musicfile()
    #read music folder
    for path_music in paths_music:
        file_extension=return_extension(path_music)
        if file_extension=="m4a":
            music_data=read_fileplace.get_musicdata_m4a(path_music)
        else:
            music_data=read_fileplace.get_musicdata_mp3(path_music)

        read_fileplace.insert_musicdata(music_data)

def get_one_column_data_list(table_name, column_name):
    return read_fileplace.get_one_column_data_list(table_name, column_name)

if __name__=="__main__":
    #if "sqlite3.OperationalError: no such table: musics"
    #read_fileplace.create_db()
    read_database()
    pagelist=list(set(read_fileplace.get_one_column_data_list("musics", "album")))

    selector=st.sidebar.selectbox("Albums", pagelist)
    print(pagelist)
    if selector==[0]:
        #play music
        file_name="sample.m4a"
        file_extension=return_extension(file_name)
        st.audio(file_name, format=f"audio/{file_extension}")