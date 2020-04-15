# deezer-python
A small set of classes to conveniently access data on Deezer


See the demo folder for some examples of what you can do, for instance send around nice cover walls:
![Release Overview](https://raw.githubusercontent.com/sharst/deezer_python/master/demo/release_overview.png)

```
In [1]: from deezer_python.deezer import Deezer

In [2]: deezer = Deezer(1234567891) # your deezer ID

In [3]: album = deezer.get_favorite_albums()[0]

In [4]: album.artist.name
Out[4]: 'Hacride'

In [5]: album.name
Out[5]: 'Amoeba'

In [6]: album.tracks
Out[6]: 
[Track(Hacride - Perturbed),
 Track(Hacride - Fate),
 Track(Hacride - Vision of hate),
 Track(Hacride - Zambra (ojos de brujo cover)),
 Track(Hacride - Liquid),
 Track(Hacride - Cycle),
 Track(Hacride - Deprived of soul),
 Track(Hacride - Strength),
 Track(Hacride - Ultima necat),
 Track(Hacride - On the threshold of death)]

In [7]: album.data.keys()
Out[7]: dict_keys(['genre_id', 'record_type', 'id', 'artist', 'duration', 'label', 'release_date', 'upc', 'cover_xl', 'share', 'available', 'nb_tracks', 'genres', 'explicit_content_cover', 'fans', 'explicit_lyrics', 'link', 'cover', 'cover_big', 'tracks', 'cover_medium', 'explicit_content_lyrics', 'title', 'tracklist', 'cover_small', 'type', 'rating', 'contributors'])
```


