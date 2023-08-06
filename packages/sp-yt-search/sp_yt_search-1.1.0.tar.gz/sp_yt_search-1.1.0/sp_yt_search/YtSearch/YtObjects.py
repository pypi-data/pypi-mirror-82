from difflib import SequenceMatcher

from .Helpers import get_numbers_from_string, date_time_string_to_seconds
from .YtSettings import YtSettings

TITLE = {
    'OFFICIALS': ['(Official Video)', '(Official Music Video)'],
    'DUMP_STAMPS': ['Official Video', 'Official Music Video', 'HQ', 'HD'],
}
CHANNEL = {
    'OFFICIALS': ['Official']
}
EMPTY_BRACKETS = ['()', '( )', '[]', '[ ]', '{}', '{ }']


class YouTube:
    def __init__(self, spotify_track, video_data):
        self.SPOTIFY_TRACK = spotify_track
        self.data = self.parse_video_data(video_data)

    def parse_video_data(self, video_data):
        res = dict()
        res['id'] = video_data.get('videoId', None)
        res['channel'] = video_data.get('longBylineText', {}).get('runs', [[{}]])[0].get('text', None)
        res['url_suffix'] = video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get(
            'webCommandMetadata', {}).get('url', None)
        res['title'] = video_data.get('title', {}).get('runs', [[{}]])[0].get('text', None)
        res['url'] = self.parse_url(
            video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url',
                                                                                                                  None))
        res['duration'] = self.parse_duration(video_data.get('lengthText', {}).get('simpleText', 0))
        res['views'] = self.parse_views(video_data.get('viewCountText', {}).get('simpleText', 0))
        res['search_ratio'] = self.count_search_ratio(res)
        res['save_path'] = self.parse_path(self.SPOTIFY_TRACK['full_name'])
        return res

    def parse_url(self, url):
        return f'{YtSettings().YT_BASE_URL}{url}'

    def parse_duration(self, duration):
        return date_time_string_to_seconds(duration)

    def parse_views(self, views):
        return get_numbers_from_string(views)

    def parse_filename(self, title):
        # remove dump stamps
        for dump_stamp in TITLE['DUMP_STAMPS']:
            title = title.replace(dump_stamp, '')
        # removes multiple spaces
        title = ' '.join(title.split())
        # returns value without leading and trailing space and mp3 extension
        for dump_stamp in EMPTY_BRACKETS:
            title = title.replace(dump_stamp, '')

        return title.strip()

    def count_search_ratio(self, res):
        search_ratio = dict()

        search_ratio['title'] = self.rate_title(res['title'].lower())
        if search_ratio['title'] >= 0.6:
            search_ratio['channel'] = self.rate_channel(res['channel'].lower())
        search_ratio['duration'] = self.rate_duration(res['duration'])

        search_ratio['whole'] = sum(search_ratio.values())
        return search_ratio['whole']

    def rate_title(self, title_lowercase):
        rate = round(SequenceMatcher(None, title_lowercase, self.SPOTIFY_TRACK['full_name'].lower()).ratio(),
                     2)
        if self.SPOTIFY_TRACK['is_official'] and any(
                official in title_lowercase for official in TITLE['OFFICIALS']):
            rate += YtSettings().BONUS_RATES['OFFICIAL']
        if self.SPOTIFY_TRACK['is_remix'] and 'remix' in title_lowercase:
            rate += YtSettings().BONUS_RATES['REMIX']
        if self.SPOTIFY_TRACK['is_instrumental'] and 'instrumental' in title_lowercase:
            rate += YtSettings().BONUS_RATES['INSTRUMENTAL']
        if self.SPOTIFY_TRACK['is_live'] and 'live' in title_lowercase:
            rate += YtSettings().BONUS_RATES['LIVE']
        return rate

    def rate_channel(self, channel_lowercase):
        rate = round(
            SequenceMatcher(None, channel_lowercase, self.SPOTIFY_TRACK['full_name'].lower()).ratio(), 2)
        if any(official in channel_lowercase for official in CHANNEL['OFFICIALS']):
            rate += YtSettings().BONUS_RATES['CHANNEL']
        return rate

    def rate_duration(self, duration):
        return 1 - (abs(duration - self.SPOTIFY_TRACK['duration']) / 100)

    def to_dict(self):
        return self.data
