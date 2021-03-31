import os
from threading import Thread
import time
from .step import Step
from pytube import YouTube
from yt_concate.setting import VIDEOS_DIR
# 多線程有排隊拿票的感覺，下載過程中一個線程發現有檔案存在，就趕快再要求另外一個
# 有明顯感覺效率增加

class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        threads = []
        for i in range(3):
            print('registering process %d' % i)
            threads.append(Thread(target=self.download_yt, args = (data[i::4], inputs, utils)))
            # 必須要用 args=() 來做參數傳遞，否則全部跑完才會跳到第二個process
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_yt(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('videos to download', len(yt_set))

        for yt in yt_set:
            url = yt.url

            if utils.video_file_exist(yt):
                print(f'found existing video file for {url}, skipping')
                continue

            if int(len([name for name in os.listdir(VIDEOS_DIR) if os.path.isfile(os.path.join(VIDEOS_DIR, name))])) > inputs['limit']:
                print('the numbers of videos are up to 20!!!')
                break
            # 因為檔案下載太慢，設條件限制資料夾內影片數量，停止下載
            # 程式碼來源：https://www.itread01.com/content/1549581703.html
            else:
                print('downloading', url)
                YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
