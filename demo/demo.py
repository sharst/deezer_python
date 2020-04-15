import datetime
from deezer_python.deezer import Deezer


if __name__ == '__main__':
    deezer_id = input("Please provide your deezer ID: ")
    deezer = Deezer(deezer_id)
    search_time = datetime.datetime(2019,1,1)

    artists = deezer.get_favorite_artists()
    for artist in artists:
        albums = artist.get_all_albums()
        for album in albums:
            if datetime.datetime.strptime(album.release_date, '%Y-%m-%d') > search_time:
                print("{} by {} was released on {}"\
                      .format(album.title, artist.name, album.release_date))
