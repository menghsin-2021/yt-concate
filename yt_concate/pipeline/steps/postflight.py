from .step import Step

class Postflight(Step):
    def process(self, data, inputs, utils):
        if inputs['cleanup'] == True:
            print('in Postflight')
            if utils.output_video_file_exist(data):
                print('found existing output file')
                utils.remove_dirs()
                utils.create_dirs_final()
            else:
                pass