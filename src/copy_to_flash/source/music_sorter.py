import logging, sys
from typing import List

from pymediainfo import MediaInfo
from operator import itemgetter

from copier import SourceFile
from .dir import DirSource, Sorter


def _name_filter(track):
    name = None
    artist = None
    is_audio = False
    if 'track_type' in track and track['track_type'] == 'Audio':
        is_audio = True
    if 'title' in track and track['title']:
        name = track['title']
    if 'performer' in track and track['performer']:
        artist = track['performer']
    return is_audio, name, artist


class MusicTrackSorter(Sorter):
    def __init__(self, filter=_name_filter, reverse=False):
        self.__reverse = reverse
        self.__filter = filter
        self.__path_list = []

    def process_path(self, path: str):
        logging.debug("process path: {}".format(path))
        try:
            info = MediaInfo.parse(path).to_data()
        except:
            the_type, the_value, _ = sys.exc_info()
            logging.debug("media info not parsed: {}/{}".format(the_type, the_value))
            return None
        if not info:
            return None
        sort_value = None
        save = False
        artist_value = None
        for track in info['tracks']:
            is_save, value, artist = self.__filter(track)
            if is_save:
                save = True
            if value:
                sort_value = value
            if artist:
                artist_value = artist
        logging.debug("sorting_value={}; save={} artist_val={}".format(sort_value, save, artist_value))
        if sort_value and save:
            self.__path_list.append({'path': path, 'title': sort_value, 'artist': artist_value})
        return None

    def sort(self) -> List[SourceFile]:
        self.__path_list.sort(key=itemgetter('title'), reverse=self.__reverse)
        res = []
        for p in self.__path_list:
            logging.debug("add to result list: {}".format(p['path']))
            res.append(SourceFile(p['path'], attr1=p['artist'], attr2=p['title']))
        return res

class MusicDirSource(DirSource):
    def __init__(self, dir_path: str):
        super().__init__(dir_path, MusicTrackSorter())