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

            print('downloading', url)
            YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)

        return data
