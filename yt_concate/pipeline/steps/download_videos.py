import os
from .step import Step
from pytube import YouTube
from yt_concate.setting import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):

        yt_set = set([found.yt for found in data])
        print('videos to download', len(yt_set))

        for yt in yt_set:
            url = yt.url

            if utils.video_file_exist(yt):
                print(f'found existing video file for {url}, skipping')
                continue

            if int(len([name for name in os.listdir(VIDEOS_DIR) if os.path.isfile(os.path.join(VIDEOS_DIR, name))])) > inputs['limit']:
                print('the numbers of videos are up to 3!!!')
                break
            # 因為檔案下載太慢，設條件限制資料夾內影片數量，停止下載
            # 程式碼來源：https://www.itread01.com/content/1549581703.html
            else:
                print('downloading', url)
                YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)

        return data
