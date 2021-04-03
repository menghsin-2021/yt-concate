import sys
sys.path.append('../')
import getopt
import logging
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


def config_logger(loglevel):
    # create logger
    logger = logging.getLogger('mainModule')
    logger.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # file handler
    # create file handler and set level to debug
    file_handler = logging.FileHandler('run_information.log')
    file_handler.setLevel(logging.DEBUG)
    # add formatter to file_handler
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # stream handler
    # create stream handler and set level to WARNING (OR user decide)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(loglevel)
    # add formatter to stream_handler
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger  # 可以不用


def print_usage():
    print('python main.py -c <channel_id> -s <search_word> -l <int(limit)>')
    print('python main.py'
          '--channel_id <channel_id>'
          '--search_word <word>'
          '--limit <number>'
          '--cleanup <True/False>'
          '--fast <True/False>'
          '--log <DEBUG/INFO/WARNING/ERROR/CRITICAL>'
          )

    print('python3 main.py OPTIONS')
    print('OPTIONS: ')
    print('{:>6} {:<12}{}'.format('', '--cleanup', 'Remove captions and video dowloaded during run.'))
    print('{:>6} {:<12}{}'.format('', '--fast', 'skip downloaded captions and videos.'))
    print('{:>6} {:<12}{}'.format('', '--log', 'set the level of logger showed on stream.'))


def main():
    CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'  # 頻道 id
    WORD = 'incredible'  # 要搜尋的字/詞
    LIMIT = 4  # 合併影片的最高片段數量
    loglevel = logging.WARNING

    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': WORD,
        'limit': LIMIT,
        'cleanup': False,  # 結果檔產生後，刪除程式執行中產生的檔案，如下載的影片/字幕等
        'fast': True,  # 跳過重複下載
        'loglevel': loglevel
    }

    short_opts = 'hc:s:l:'
    long_opts = 'help channel_id= search_word= limit= cleanup= fast= log='.split()

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
        elif opt in ('--log'):
            inputs['loglevel'] = eval(f'logging.{arg}')

    print('CHANNEL_ID is ', inputs['channel_id'])
    print('WORD is ', inputs['search_word'])
    print('LIMIT is ', inputs['limit'])
    print('cleanup is ', inputs['cleanup'])
    print('fast is ', inputs['fast'])
    print('log level is ', inputs['loglevel'])

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

    config_logger(inputs['loglevel'])
    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
