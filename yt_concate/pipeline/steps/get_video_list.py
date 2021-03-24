import urllib.request
import json
from yt_concate.setting import API_KEY
from yt_concate.pipeline.steps.step import Step


class GetVideoList(Step):
    def process(self, data, inputs):
        channel_id = inputs['channel_id']  # 預計做一個字典放在 main，把未來需要 input 的東西打包起來，之後都用字典 call 需要的東西
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
        print(video_links)
        return video_links
