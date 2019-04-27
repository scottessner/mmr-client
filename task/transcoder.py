import os
import re
import subprocess
from task.base import Task


class TranscodeTask(Task):

    def __init__(self, url, base_path, task_content):
        self.progress_regex = re.compile('Encoding:.*, (?P<progress>\d{0,3}).* \((?P<fps>.{0,6}) fps, avg (?P<fps_avg>.{0,6}) fps.*(?P<hours>\d{2})h(?P<minutes>\d{2})m(?P<seconds>\d{2})s\)')
        super().__init__(url, base_path, task_content)

    def find_transcode_progress(self, line):
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

            command = ['HandBrakeCLI',
                       '-i',
                       self.source_path,
                       '-o',
                       self.tmp_path,
                       '--preset=HQ 1080p30 Surround',
                       '--subtitle',
                       'scan',
                       '-F']

            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE,
                                       stderr=logfile)

            progress = dict()
            while True:
                line = ''
                while line[-1:] != '\r' and process.poll() is None:
                    line = line + bytes.decode(process.stdout.read(1))

                latest_progress = self.find_transcode_progress(line)
                if progress.get('progress', None) != latest_progress.get('progress', None):
                    progress = latest_progress
                    # print(line)
                    if progress.get('progress', None):
                        self.set_progress(progress['progress'])
                        # print('Transcoding: {}% Complete ETA: {}'.format(progress['progress'], progress['eta']))

                if process.poll() is not None:
                    if process.poll() == 0:
                        print('Compressed Successfully.')
                        os.rename(self.tmp_path, self.dest_path)
                        os.remove(self.source_path)
                        self.complete()
                    else:
                        self.error()
                    logfile.write('HandBrakeCLI completed with return code {}'.format(process.poll()))

                    return process.poll()


# if __name__ == '__main__':
#     url = 'http://127.0.0.1:5000/v1'
#     # url = 'http://ssessner.com/mmr-api/v1'
#
#     client = TaskClient(url, '/data/media')
#
#     while True:
#         client.take()
#
#         if client.task:
#             print('Compressing: {}'.format(client.task['source_path']))
#             status = transcode(client)
#         else:
#             time.sleep(60)
