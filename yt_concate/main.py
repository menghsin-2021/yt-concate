import sys
sys.path.append('../')
import getopt
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils





def print_usage():
    print('python main.py -c <channel_id> -s <search_word> -l <int(limit)>')
    print('python main.py --channel_id <channel_id> '
          '--search_word <search_word> --'
          '--limit <int(limit)>'
          '--cleanup <True/False>'
          '--fast <True/False>'
          )

    print('python3 main.py OPTIONS')
    print('OPTIONS: ')
    print('{:>6} {:<12}{}'.format('', '--cleanup', 'Remove captions and video dowloaded during run.'))
    print('{:>6} {:<12}{}'.format('', '--fast', 'skip downloaded captions and videos.'))

def main():
    CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'  # 頻道 id
    WORD = 'incredible'  # 要搜尋的字/詞
    LIMIT = 19  # 合併影片的最高片段數量

    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': WORD,
        'limit': LIMIT,
        'cleanup': False,  # 結果檔產生後，刪除程式執行中產生的檔案，如下載的影片/字幕等
        'fast': True,  # 跳過重複下載
    }

    short_opts = 'hc:s:l:'
    long_opts = 'help channel_id= search_word= limit= cleanup= fast='.split()

    print(sys.argv[1:])
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)  # 用 opts 解析 argv 所投入的參數 ，投遞只能印出檔名後的東西
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel_id'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--search_word'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            inputs['limit'] = int(arg)
        elif opt in ('--cleanup'):
            inputs['cleanup'] = bool(arg)
        elif opt in ('--fast'):
            inputs['fast'] = bool(arg)

    print('CHANNEL_ID is ', inputs['channel_id'])
    print('WORD is ', inputs['search_word'])
    print('LIMIT is ', inputs['limit'])
    print('cleanup is ', inputs['cleanup'])
    print('fast is ', inputs['fast'])

    if not CHANNEL_ID or not WORD:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
