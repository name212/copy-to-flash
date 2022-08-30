from typing import List

from pymediainfo import MediaInfo
from operator import itemgetter
from .dir import Sorter


def _name_filter(track):
    name = None
    is_audio = False
    if 'track_type' in track and track['track_type'] == 'Audio':
        is_audio = True
    if 'title' in track and track['title']:
        name = track['title']

    return is_audio, name


class MusicTrackSorter(Sorter):
    def __init__(self, filter=_name_filter, reverse=False):
        self.__reverse = reverse
        self.__filter = filter
        self.__path_list = []

    def process_path(self, path: str):
        try:
            info = MediaInfo.parse(path).to_data()
        except:
            return None
        if not info:
            return None
        sort_value = None
        save = False
        for track in info['tracks']:
            is_save, value = self.__filter(track)
            if is_save:
                save = True
            if value:
                sort_value = value

        if sort_value and save:
            self.__path_list.append({'path': path, 'sort': sort_value})
        return None

    def sort(self) -> List[str]:
        self.__path_list.sort(key=itemgetter('sort'), reverse=self.__reverse)
        return [p['path'] for p in self.__path_list]
