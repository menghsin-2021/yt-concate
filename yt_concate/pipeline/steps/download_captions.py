import os
from multiprocessing import Process
import time
from pytube import YouTube
from .step import Step
from .step import StepException
# 多進程變得像一起下載同個東西(好像沒有比較快)，搶著下載同個檔案
# 但如果把要下載的所有檔案平均分配給各個 process 應該會快很多

class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        processes = []
        for i in range(6):
            print('registering process %d' % i)
            processes.append(Process(target=self.download_cap, args=(data, inputs, utils)))
            # 必須要用 args=() 來做參數傳遞，否則全部跑完才會跳到第二個process

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_cap(self, data, inputs, utils):
        for yt in data:
            print('downloading caption for', yt.id)
            if utils.caption_file_exist(yt):
                print('found existing caption file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())

            except AttributeError:
                print('AttributeError when downloading caption for', yt.url)
                continue

                # print(en_caption_convert_to_srt)
            text_file = open(yt.get_caption_filepath(), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

