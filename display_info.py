import read_fileplace
import pprint
#database data sort by album
def list_sort_by_album(albums_list):
    album_dic={}
    #["album1", "album2", "album3"]
    albums=list(set(read_fileplace.get_one_column_data_list("musics", "album")))

    for i, album in enumerate(albums):
            for i, music in enumerate(albums_list):
                if album==albums_list[i]["album"]:
                    #append same album name
                    album_dic.setdefault(album, []).append(music)

    return album_dic


pprint.pprint(list_sort_by_album(read_fileplace.get_one_row_data_list("musics")))