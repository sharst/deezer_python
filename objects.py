import datetime
import urllib.request

from .util import retried_get


class DeezerObj(object):
    API_DIR = ''

    def __init__(self, data):
        self.data = data

    def __getattr__(self, attrib):
        if attrib in self.__dict__:
            self.__dict__[attrib]
        else:
            return self.data[attrib]

    def reload_all_fields(self):
        """ Refetch all information again from the api.
            This is particularly useful if only part of the info has been fetched
            before, e.g. if a track has been created as part of a playlist """
        url = "https://api.deezer.com/{}/{}".format(self.API_DIR, self.id)
        data = retried_get(url)
        self.__init__(data)


class Track(DeezerObj):
    API_DIR = 'track'

    def __init__(self, data):
        super(Track, self).__init__(data)
        self.artist = Artist(self.data['artist'])

        if not isinstance(self.duration, datetime.timedelta):
            self.duration = datetime.timedelta(seconds=self.duration)

        if "contributors" in self.data:
            self.contributors = [Artist(contrib) for contrib in self.contributors]

    def download_preview(self, target_path):
        preview_url = self.data.get('preview', None)
        if preview_url:
            filedata = urllib.request.urlopen(preview_url)
            with open(target_path, 'wb') as mfile:
                mfile.write(filedata.read())
                return True
        else:
            return False

    def safe_filename(self, name_format):
        """ Returns a filename suggestion for this track that is safe to
            use on NTFS drives (omits the use of special characters, like * """
        filename = name_format.format(artist=self.artist.name,
                                      title=self.title)
        not_allowed = '*/\\:?"<>|'
        filename = ''.join(["-" if f in not_allowed else f for f in filename])
        return filename

    def __repr__(self):
        return 'Track({} - {})'.format(self.artist.name, self.title)


class Artist(DeezerObj):
    API_DIR = 'artist'

    def __repr__(self):
        return 'Artist({})'.format(self.name)

    def get_all_albums(self):
        objects = []
        url = "https://api.deezer.com/artist/{}/albums".format(self.id)
        while True:
            resp = retried_get(url)
            objects += [Album(data) for data in resp['data']]
            if resp.get('next'):
                url = resp['next']
            else:
                break
        return objects


class Album(DeezerObj):
    API_DIR = 'album'

    def __init__(self, data):
        super(Album, self).__init__(data)
        if 'artist' in self.data:
            self.artist = Artist(self.data['artist'])
        if 'tracks' in self.data:
            self.tracks = [Track(track) for track in self.data['tracks']['data']]

    def __repr__(self):
        return 'Album({} - {})'.format(self.artist.name, self.title)


class Playlist(DeezerObj):
    def __init__(self, data):
        data = retried_get("https://api.deezer.com/playlist/{}".format(data['id']))
        super(Playlist, self).__init__(data)
        self.tracks = [Track(track) for track in data['tracks']['data']]

    def __repr__(self):
        return 'Playlist({})'.format(self.title)
