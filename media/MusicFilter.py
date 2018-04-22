from pymediainfo import MediaInfo


class MusicFileFilter(object):
    def __call__(self, path):
        try:
            info = MediaInfo.parse(path).to_data()
        except:
            return None
        if not info:
            return None
        name = None
        is_audio = False
        for track in info['tracks']:
            if 'track_type' in track and track['track_type'] == 'Audio':
                is_audio = True
            if 'title' in track and track['title']:
                name = track['title']
        if not name or not is_audio:
            return None

        return {'path': path, 'name': name}