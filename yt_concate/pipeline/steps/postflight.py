import logging
from .step import Step

class Postflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'mainModule.{__name__}')
        if inputs['cleanup'] == True:
            logger.info('in Postflight')
            if utils.output_video_file_exist(data):
                logger.info('found existing output file')
                utils.remove_dirs()
                utils.create_dirs_final()
            else:
                pass