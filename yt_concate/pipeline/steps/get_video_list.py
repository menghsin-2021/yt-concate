import urllib.request
import json
import logging
from yt_concate.setting import API_KEY
from yt_concate.pipeline.steps.step import Step


class GetVideoList(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'mainModule.{__name__}')
        channel_id = inputs['channel_id']  # 預計做一個字典放在 main，把未來需要 input 的東西打包起來，之後都用字典 call 需要的東西

        if utils.video_list_file_exits(channel_id):
            logger.info(f'found existing video list file for channel id {channel_id}')
            return self.read_file(utils.get_video_list_filepath(channel_id))

        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(API_KEY,
                                                                                                            channel_id)

        video_links = []
        url = first_url
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)

            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])

            try:
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
            except KeyError:
                break
        logger.info(video_links)
        self.write_to_file(video_links, utils.get_video_list_filepath(channel_id))
        return video_links

    def write_to_file(self, video_links, filepath):
        with open(filepath, 'w') as f:
            for url in video_links:
                f.write(url + '\n')

    def read_file(self, filepath):
        video_links = []
        with open(filepath, 'r') as f:
            for url in f:
                video_links.append(url.strip())
        return video_links
