import logging
from .step import Step
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips


class EditVideo(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'mainModule.{__name__}')
        clips = []
        for found in data:
            logger.info(found.time)
            logger.info(found.yt)
            start, end = self.parse_caption_time(found.time)
            try:
                video = VideoFileClip(found.yt.get_video_filepath()).subclip(start, end)
            except OSError:
                logger.warning('no video')
                continue
            # 因為影片太少會出錯找不到路徑 目前先 skip 掉這個步驟
            clips.append(video)
            if len(clips) >= inputs['limit']:
                break
        output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_filepath)

        # closing VideoFileClips
        for video in clips:
            video.close()

        return output_filepath

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h), int(m), int(s) + int(ms)/1000