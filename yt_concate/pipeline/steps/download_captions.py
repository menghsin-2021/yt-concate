import sys
sys.path.append('C:\\Users\\Meng-Hsin\\venv\\lib\\site-packages')
import concurrent.futures
import time
from pytube import YouTube
from .step import Step
from .step import StepException
# 多進程變得像一起下載同個東西(好像沒有比較快)

class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        YT = []
        for yt in data:
            print('downloading caption for', yt.id)
            if utils.caption_file_exist(yt) and inputs['fast'] == True:
                print('found existing caption file')
                pass
            else:
                YT.append(yt)

        for yt in YT:
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                executor.submit(self.download_cap, yt, inputs, utils)

        end = time.time()
        print('took', end - start, 'seconds')

        return data

    def download_cap(self, yt, inputs, utils):
        try:
            source = YouTube(yt.url)
            en_caption = source.captions.get_by_language_code('a.en')
            en_caption_convert_to_srt = (en_caption.generate_srt_captions())
            text_file = open(yt.get_caption_filepath(), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()
        except AttributeError:
            print('AttributeError when downloading caption for', yt.url)



