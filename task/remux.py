import os
import re
import subprocess
from task.base import Task


class RemuxTask(Task):

    def __init__(self, url, task_content):
        self.progress_regex = re.compile('frame=*(?P<frame>\d{0,6})\sfps=\s(?P<fps>\d{0,6}).*time=(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}).(?P<ms>\d{2})\sbitrate=(?P<bitrate>.*(?=kbits/s)).*speed=(?P<speed>.*(?=x))')
        super().__init__(url, task_content)

    @Task.dest_path.getter
    def dest_path(self):
        return '{}{}'.format(os.path.splitext(self.source_path)[0], '.mp4')

    # TODO: Establish progress measurement for remux
    def find_remux_progress(self, line):
        result = self.progress_regex.match(line)
        progress = dict()
        if result is not None:
            progress['progress'] = result.groupdict().get('progress', None)
            progress['hours'] = result.groupdict().get('hours', None)
            progress['minutes'] = result.groupdict().get('minutes', None)
            progress['seconds'] = result.groupdict().get('seconds', None)
            progress['eta'] = '{}:{}:{}'.format(progress['hours'], progress['minutes'], progress['seconds'])
        return progress

    def execute(self):

        self.start()

        folder = os.path.split(self.tmp_path)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.log_path, 'w+') as logfile:

            command = ['ffmpeg',
                       '-y',
                       '-i',
                       self.source_path,
                       '-c',
                       'copy',
                       self.tmp_path]

            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            progress = dict()
            while True:
                line = ''
                while line[-1:] != '\r' and process.poll() is None:
                    line = line + bytes.decode(process.stderr.read(1))
                # line = bytes.decode(process.stderr.readline())

                latest_progress = self.find_remux_progress(line)
                if progress.get('progress', None) != latest_progress.get('progress', None):
                    progress = latest_progress

                # TODO Build out progress update to server

                # print(line)
                #     if progress.get('progress', None):
                #         client.set_progress(progress['progress'])
                #         # print('Transcoding: {}% Complete ETA: {}'.format(progress['progress'], progress['eta']))

                if process.poll() is not None:
                    if process.poll() == 0:
                        print('Remuxed Successfully.')
                        os.rename(self.tmp_path, self.dest_path)
                        os.remove(self.source_path)
                        self.update_title_path(self.dest_path)
                        self.complete()
                    else:
                        self.error()
                    logfile.write('ffmpeg completed with return code {}'.format(process.poll()))

                    return process.poll()
