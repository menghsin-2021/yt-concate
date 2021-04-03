from .step import Step
import logging

class Preflight(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger(f'mainModule.{__name__}')
        logger.info('in Preflight')
        utils.create_dirs()