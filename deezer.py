from .objects import Playlist, Album, Artist
from .util import retried_get


class Deezer(object):
    def __init__(self, user_id):
        """ Instatiate the class with your Deezer user ID
            In order to find it, go to your profile on Deezer.com
            Your user id is the number in the address bar:
            https://www.deezer.com/us/profile/XXXXXXXX """
        self.user_id = user_id

    def get_playlists_by_keyword(self, keyword):
        url = "https://api.deezer.com/user/{}/playlists".format(self.user_id)
        pls = []
        while True:
            resp = retried_get(url)
            pls += [Playlist(pl) for pl in resp['data']
                    if keyword in pl['title']]
            if resp.get('next'):
                url = resp['next']
            else:
                break
        return pls

    def get_playlists_by_name(self, names):
        return [pl for pl in self.get_playlists()
                if pl['title'] in names]

    def get_playlists(self):
        url = "https://api.deezer.com/user/{}/playlists".format(self.user_id)
        return self.request_all_objects_from_url(Playlist, url)

    def get_playlist(self, name):
        pls = self.get_playlists()
        return next((pl for pl in pls
                     if pl.title == name), None)

    def request_all_objects_from_url(self, obj_class, url):
        objects = []
        while True:
            resp = retried_get(url)
            objects += [obj_class(data) for data in resp['data']]
            if resp.get('next'):
                url = resp['next']
            else:
                break
        return objects

    def get_favorite_artists(self):
        url = "https://api.deezer.com/user/{}/artists".format(self.user_id)
        return self.request_all_objects_from_url(Artist, url)

    def get_favorite_albums(self):
        url = "https://api.deezer.com/user/{}/albums".format(self.user_id)
        return self.request_all_objects_from_url(Album, url)
